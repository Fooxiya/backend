from rest_framework.viewsets import ModelViewSet
from .serializers import UserModelSerializer
from .models import User
from rest_framework.serializers import Serializer, CharField, EmailField


class UserViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()


class UserSerializer(Serializer):

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user

    first_name = CharField(max_length=64)
    last_name = CharField(max_length=64)
    email = EmailField()
