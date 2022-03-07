from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import UserModelSerializer, UserSerializer
from .models import User


class UserViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()


class UserModelViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListView(ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveView(RetrieveAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = UserSerializer
    queryset = User.objects.all()
