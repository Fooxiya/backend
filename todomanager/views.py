import io

from rest_framework.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.fields import DateField, BooleanField
from rest_framework.serializers import Serializer, CharField
from rest_framework.viewsets import ModelViewSet
from .serializers import ProjectModelSerializer, TodoModelSerializer
from authapp.serializers import UserModelSerializer
from authapp.views import UserSerializer
from authapp.models import User
from .models import Project, Todo
from django.http import HttpResponse, HttpResponseServerError
from rest_framework.parsers import JSONParser


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectModelSerializer
    queryset = Project.objects.all()


class TodoViewSet(ModelViewSet):
    serializer_class = TodoModelSerializer
    queryset = Todo.objects.all()


class ProjectSerializer(Serializer):
    name = CharField(max_length=64)
    link = CharField(max_length=128)
    users = UserModelSerializer(many=True)


class TodoSerializer(Serializer):
    project = ProjectSerializer()
    text = CharField(max_length=128)
    creation_date = DateField
    update_date = DateField
    user = UserModelSerializer(many=True)
    status = BooleanField


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
