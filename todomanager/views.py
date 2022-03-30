import io

from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import ProjectModelSerializer, TodoModelSerializer, ProjectSerializer, TodoSerializer
from authapp.serializers import UserModelSerializer, UserSerializer
from authapp.models import User
from .models import Project, Todo
from django.http import HttpResponse, HttpResponseServerError
from rest_framework.parsers import JSONParser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status


class ProjectLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10


class ProjectModelViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    pagination_class = ProjectLimitOffsetPagination


class TodoLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20


class TodoModelViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    pagination_class = TodoLimitOffsetPagination

    def destroy(self, request, *args, **kwargs):
        try:
            todo = self.get_object()
            todo.is_active = False
            todo.save()
            return Response(status=status.HTTP_200_OK)
        except IntegrityError:
            content = {'error': 'IntegrityError'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectModelSerializer
    queryset = Project.objects.all()


class TodoViewSet(ModelViewSet):
    serializer_class = TodoModelSerializer
    queryset = Todo.objects.all()


class ProjectListView(ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ProjectRetrieveView(RetrieveAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class TodoListView(ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()


class TodoRetrieveView(RetrieveAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def project_api_view(request):
    project = Project.objects.all()
    serializer = ProjectSerializer(project, many=True)
    return Response(serializer.data)


def get_view(request):
    project = Project.objects.get(pk=1)
    serializer = ProjectSerializer(project)
    render = JSONRenderer()
    json_data = render.render(serializer.data)
    return HttpResponse(json_data)


@csrf_exempt
def post_view(request):
    data = JSONParser().parse(io.BytesIO(request.body))

    if request.method == 'POST':
        serializer = UserSerializer(data=data)
    elif request.method == 'PUT':
        user = User.objects.get(pk=3)
        serializer = UserSerializer(user, data=data)
    elif request.method == 'PATCH':
        user = User.objects.get(pk=3)
        serializer = UserSerializer(user, data=data, partial=True)

    if serializer.is_valid():
        print(serializer.validated_data)

        user = serializer.save()
        return render_user(user)
    else:
        return HttpResponseServerError(serializer.errors['non_field_errors'])


def render_user(user):
    serializer = UserSerializer(user)
    render = JSONRenderer()
    json_data = render.render(serializer.data)
    return HttpResponse(json_data)
