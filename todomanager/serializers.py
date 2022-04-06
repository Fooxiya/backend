from rest_framework.fields import DateField, BooleanField
from rest_framework.serializers import ModelSerializer
from authapp.serializers import UserModelSerializer
from .models import Project, Todo
from rest_framework.serializers import Serializer, CharField


class ProjectModelSerializer(ModelSerializer):
    users = UserModelSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'


class TodoModelSerializer(ModelSerializer):
    user = UserModelSerializer(many=True)

    class Meta:
        model = Todo
        fields = '__all__'


class ProjectSerializer(Serializer):

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.link = validated_data.get('link', instance.link)
        instance.users = validated_data.get('user', instance.users)
        instance.save()
        return instance

    def create(self, validated_data):
        project = Project(**validated_data)
        project.save()
        return project

    name = CharField(max_length=64)
    link = CharField(max_length=128)
    users = UserModelSerializer(many=True)


class ProjectSerializerBase(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TodoSerializer(Serializer):

    def update(self, instance, validated_data):
        instance.project = validated_data.get('project', instance.project)
        instance.text = validated_data.get('text', instance.text)
        instance.creation_date = validated_data.get('creation_date', instance.creation_date)
        instance.update_date = validated_data.get('update_date', instance.update_date)
        instance.user = validated_data.get('user', instance.user)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    def create(self, validated_data):
        todo = Todo(**validated_data)
        todo.save()
        return todo

    project = ProjectSerializer()
    text = CharField(max_length=128)
    creation_date = DateField
    update_date = DateField
    user = UserModelSerializer(many=True)
    is_active = BooleanField(default=True)
