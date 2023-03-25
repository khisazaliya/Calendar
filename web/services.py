import csv


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

