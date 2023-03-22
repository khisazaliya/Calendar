from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskTag(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=256, verbose_name = 'Название')
    description = models.TextField(verbose_name = 'Описание')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Пользователь')
    tags = models.ManyToManyField(TaskTag, verbose_name = 'Теги')
    image = models.ImageField(upload_to='tasks/', null=True, blank=True, verbose_name = 'Изображение')

