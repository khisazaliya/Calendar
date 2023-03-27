import random
from datetime import timedelta
from random import randint

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from web.models import Task, User, TaskTag


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.last()
        tags = TaskTag.objects.filter(user = user)

        tasks = []

        for day_index in range(30):

            for task_index in range(randint(5, 10)):
                tasks.append(Task(
                    title = f'generated {day_index}-{task_index}',
                    user = user
                ))

        Task.objects.bulk_create(tasks)
