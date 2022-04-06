from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from .views import ProjectViewSet
from .models import Project


class TestProjectViewSet(TestCase):

    def test_get_list(self):
        factory = APIRequestFactory()
        request = factory.get('/api/projects/')
        view = ProjectViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail(self):
        project = Project.objects.create(name='Test', link='TestLink')
        client = APIClient()
        response = client.get(f'/api/projects/{project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestProjectApi(APITestCase):

    def setUP(self) -> None:
        project = mixer.blend(Project)
        self.admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123456')
        self.client.login(username='admin', password='admin123456')
        response = self.client.put(f'/api/projects/{project.id}/',
                                   {'name': 'Test', 'link': 'TestLink', 'users': project.users.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(project.name, 'Test')

    def test_get_list(self):
        self.client.login(username='admin', password='admin123456')
        self.client.logout()
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_1(self):
        response = self.client.get('api/projects')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
