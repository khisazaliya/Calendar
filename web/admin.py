from django.contrib import admin
from web.models import Task, TaskTag


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', "user", 'description')
    search_fields = ("id", "title")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate_description()

    @admin.display(description = 'Описание')
    def get_description(self, instance):
        return instance.description


class TaskTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', "user")
    search_fields = ("id", "title")


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskTag, TaskTagAdmin)


# Register your models here.
