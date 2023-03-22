from django.urls import path

from web.views import main_view, registration_view, auth_view, logout_view, task_edit_view

urlpatterns = [
    path("", main_view, name = "main"),
    path("registration/", registration_view, name = "registration"),
    path("auth/", auth_view, name = "auth"),
    path("logout/", logout_view, name = "logout"),
    path("tasks/add/", task_edit_view, name = "tasks_add"),
    path("tasks/<int:id>", task_edit_view, name = "tasks_edit")
]
