from django.urls import path

from web.views import main_view, registration_view, auth_view, logout_view, task_edit_view, tags_view, tags_delete_view, \
    tasks_delete_view, analytics_view

urlpatterns = [
    path("", main_view, name = "main"),
    path("analytics/", analytics_view, name = "analytics"),
    path("registration/", registration_view, name = "registration"),
    path("auth/", auth_view, name = "auth"),
    path("logout/", logout_view, name = "logout"),
    path("tasks/add/", task_edit_view, name = "tasks_add"),
    path("tasks/<int:id>", task_edit_view, name = "tasks_edit"),
    path("tasks/<int:id>/delete/", tasks_delete_view, name = "tasks_delete"),
    path("tags", tags_view, name = "tags"),
    path("tags/<int:id>/delete/", tags_delete_view, name = "tags_delete"),
]
