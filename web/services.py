import csv

from web.models import Task, TaskTag


def filter_tasks(tasks_qs, filters: dict):
    if filters['search']:
        tasks = tasks_qs.filter(title__icontains = filters['search'])
    return tasks_qs


def export_tasks_csv(tasks_qs, response):
    writer = csv.writer(response)
    writer.writerow(("title", "description", "tags"))

    for task in tasks_qs:
        writer.writerow((
            task.title, task.description,
            " ".join([t.title for t in task.tags.all()]),
        ))

    return response


def import_tasks_from_csv(file, user_id):
    strs_from_file = (row.decode() for row in file)
    reader = csv.DictReader(strs_from_file)

    tasks = []
    task_tags = []
    for row in reader:
        tasks.append(Task(
            title = row['title'],
            description = row['description'],
            user_id = user_id
        ))
        task_tags.append(row['tags'].split(" ") if row['tags'] else [])

    saved_tasks = Task.objects.bulk_create(tasks)

    tags_map = dict(TaskTag.objects.all().values_list("title", "id"))
    task_tags = []
    for task,  task_tags_item in zip(saved_tasks, task_tags):
        for tag in task_tags_item:
            tag_id = tags_map[tag]
            task_tags.append(
                Task.tags.through(task_id = task.id, tasktag_id = tag_id)
            )
    Task.tags.through.objects.bulk_create(task_tags)
