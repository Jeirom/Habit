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
    """ViewSet для управления привычками пользователей.

    Этот ViewSet предоставляет стандартные операции CRUD (создание, чтение, обновление, удаление)
    для модели привычки.  Включает валидацию данных при создании и обновлении, пагинацию результатов
    и проверку прав доступа, позволяя просматривать привычку либо её владельцу, либо всем,
    если привычка имеет статус публичной (is_public=True).

    Атрибуты:
        queryset: Запрос для получения всех объектов привычки.
        validators: Список валидаторов, применяемых при создании и обновлении привычки.
                    Включает валидацию на ограничение времени выполнения и периодичность.
        serializer_class: Сериализатор для модели привычки.
        pagination_class: Класс для пагинации результатов.  Выводит 5 элементов на странице.
        permission_classes: Список классов разрешений, определяющих права доступа к привычке.
                           Включает проверку на то, является ли пользователь владельцем привычки,
                           или является ли привычка публичной.

    Методы:
        public_habits(request): Возвращает список публичных привычек с применением пагинации.
    """

    queryset = Habit.objects.all()
    validators = [validate_time_limit, validate_frequency] # Проверка на периодичность выполнения привычки и времени выполнения
    serializer_class = HabitSerializer
    pagination_class = HabitPagination # Вывод 5 элементов на одной странице
    permission_classes = [IsOwnerOrPublic] # Либо владелец, либо статус привычки - публичный (is_public=True)

    @action(detail=False, methods=['get'], url_path='public')
    def public_habits(self, request):
        public_habits = self.queryset.filter(is_public=True)
        page = self.paginate_queryset(public_habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)
