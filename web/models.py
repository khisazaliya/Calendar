from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskTag(models.Model):
    title = models.CharField(256)
    user = models.ForeignKey(User, on_delete = models.CASCADE)


class Task(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(TaskTag)

