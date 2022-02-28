from django.db import models
from authapp.models import User


class Project(models.Model):
    name = models.CharField(max_length=64)
    link = models.CharField(max_length=128)
    users = models.ManyToManyField(User)


class Todo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)
    creation_date = models.DateField
    update_date = models.DateField
    user = models.ManyToManyField(User)
    status = models.BooleanField
