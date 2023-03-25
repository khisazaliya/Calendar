from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from web.forms import RegistrationForm, AuthForm, TaskForm, TaskTagForm, TaskFilterForm, ImportForm
from web.models import Task, TaskTag
from web.services import filter_tasks, export_tasks_csv, import_tasks_from_csv, get_stat

User = get_user_model()


@cache_page(10)
@login_required
def main_view(request):
    tasks = Task.objects.filter(user = request.user).order_by('title')

    filter_form = TaskFilterForm(request.GET)
    filter_form.is_valid()
    tasks = filter_tasks(tasks, filter_form.cleaned_data)

    total_count = tasks.count()
    tasks = (
        tasks
        .prefetch_related("tags")
        .select_related("user")
        .annotate(tags_count = Count("tags"))
    )

    page_number = request.GET.get("page", 1)
    paginator = Paginator(tasks, per_page = 10)

    if request.GET.get("export") == 'csv':
        response = HttpResponse(
            content_type = 'text/csv',
            headers = {"Content-Disposition": "attachment; filename=timeslots.csv"}
        )
        return export_tasks_csv(tasks, response)

    return render(request, "web/main.html", {
        'tasks': paginator.get_page(page_number),
        'form': TaskForm,
        'filter_form': filter_form,
        'total_count': total_count
    })


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data = request.POST)
        if form.is_valid():
            user = User(
                username = form.cleaned_data['username'],
                email = form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
    return render(request, "web/registration.html", {
        "form": form, "is_success": is_success
    })


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data = request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Введены неверные данные")
            else:
                login(request, user)
                return redirect("main")
    return render(request, "web/auth.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("main")


@login_required
def task_edit_view(request, id = None):
    task = get_object_or_404(Task, id = id) if id is not None else None
    form = TaskForm(instance = task)
    if request.method == 'POST':
        form = TaskForm(data = request.POST, files = request.FILES, initial = {"user": request.user})
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/task_form.html", {"form": form})


@login_required
def tasks_delete_view(request, id):
    task = get_object_or_404(Task, user = request.user, id = id)
    task.delete()
    return redirect('main')


@login_required
def tags_view(request):
    tags = TaskTag.objects.all()
    form = TaskTagForm()
    if request.method == 'POST':
        form = TaskTagForm(data = request.POST, initial = {"user": request.user})
        if form.is_valid():
            form.save()
            return redirect("tags")
    return render(request, "web/tags.html", {"tags": tags, "form": form})


@login_required
def tags_delete_view(request, id):
    tag = get_object_or_404(TaskTag, user = request.user, id = id)
    tag.delete()
    return redirect('tags')


@login_required
def analytics_view(request):
    overall_stat = Task.objects.aggregate(
        count = Count("id"),
    )

    return render(request, "web/analytics.html", {
        "overall_stat": overall_stat,
    })

    return render(request, "web/analytics.html")


@login_required
def import_view(request):
    if request.method == 'POST':
        form = ImportForm(files = request.FILES)
        if form.is_valid():
            import_tasks_from_csv(form.cleaned_data['file'], request.user.id)
            return redirect("main")
    return render(request, "web/import.html", {
        "form": ImportForm()
    })



@login_required
def stat_view(request):
    return render(request, "web/stat.html", {"results": get_stat()})