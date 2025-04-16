from urllib import request

from rest_framework.viewsets import ModelViewSet

from habit.models import Habit
from habit.paginators import HabitPagination
from habit.permissions import IsOwnerOrPublic
from habit.serializer import HabitSerializer
from habit.validators import validate_time_limit, validate_frequency


class HabitViewSet(ModelViewSet):

    queryset = Habit.objects.all()
    validators = [validate_time_limit, validate_frequency]
    serializer_class = HabitSerializer
    pagination_class = HabitPagination # Вывод 5 элементов на одной странице

    permission_classes = [IsOwnerOrPublic]


    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return CourseDetailSerializer
    #     return CourseSerializer
    #
    # def perform_create(self, serializer):
    #     lesson = serializer.save()
    #     lesson.owner = self.request.user
    #     lesson.save()
    #
    # def get_permissions(self):
    #     if self.action == 'create':
    #         self.permission_classes = (~IsModer,)
    #     elif self.action in ['update', 'retrieve']:
    #         self.permission_classes = (IsModer | IsOwner,)
    #     elif self.action == 'destroy':
    #         self.permission_classes = (IsOwner | ~IsModer,)
    #     return super().get_permissions()
