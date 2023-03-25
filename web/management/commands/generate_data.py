import random
from datetime import timedelta
from random import randint

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from web.models import Task, User, TaskTag


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.first()
        tags = TaskTag.objects.filter(user = user)

        tasks = []

        for day_index in range(30):

            for task_index in range(randint(5, 10)):
                tasks.append(Task(
                    title = f'generated {day_index}-{task_index}',
                    user = user
                ))

        # saved_tasks = Task.objects.bulk_create(tasks)
        # task_tags = []
        # for time_slot in saved_tasks:
        #     count_of_tags = randint(0, len(tags))
        #     for tag_index in range(count_of_tags):
        #         task_tags.append(
        #             Task.tags.through(timeslot_id = time_slot.id, timeslottag_id = tags[tag_index].id)
        #         )
        Task.objects.bulk_create(tasks)
