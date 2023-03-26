from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.serializers import TaskSerializer, TagSerializer
from web.models import Task, TaskTag


@api_view(["GET"])
@permission_classes([])
def main_view(request):
    return Response({"status": "ok"})


class TaskModelViewSet(ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all().select_related("user").prefetch_related("tags").filter(user=self.request.user)


class TagsViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        return TaskTag.objects.all().filter(user=self.request.user)