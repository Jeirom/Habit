from urllib import request

from django.shortcuts import render
from requests import Response
from rest_framework.decorators import action
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
    # template_name = "habit_main.html"
    # context_object_name = "habit"
    permission_classes = [IsOwnerOrPublic]

    @action(detail=False, methods=['get'], url_path='public')
    def public_habits(self, request):
        public_habits = self.queryset.filter(is_public=True)
        page = self.paginate_queryset(public_habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)



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
