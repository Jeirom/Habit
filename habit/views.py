from requests import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from habit.models import Habit
from habit.paginators import HabitPagination
from habit.permissions import IsOwnerOrPublic
from habit.serializer import HabitSerializer


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
    serializer_class = HabitSerializer
    pagination_class = HabitPagination  # Вывод 5 элементов на одной странице
    permission_classes = [
        IsOwnerOrPublic
    ]  # Либо владелец, либо статус привычки - публичный (is_public=True)

    @action(detail=False, methods=["get"], url_path="public")
    def public_habits(self, request):
        public_habits = self.queryset.filter(is_public=True)
        page = self.paginate_queryset(public_habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        self.validate_habit(serializer)
        serializer.save()

    def perform_update(self, serializer):
        self.validate_habit(serializer)
        serializer.save()

    def validate_habit(self, serializer):
        habit = serializer.validated_data

        # Проверка одновременного заполнения связанных полей
        related_habit = habit.get("related_habit")
        reward = habit.get("reward")
        if related_habit and reward:
            raise ValidationError(
                "Нельзя одновременно указывать связанную привычку и вознаграждение."
            )

        # Проверка, что только приятная привычка не указывает на связанные привычки или вознаграждение
        is_pleasant = habit.get("is_pleasant", False)
        if is_pleasant:
            if related_habit or reward:
                raise ValidationError(
                    "Приятная привычка не может иметь связанную привычку или вознаграждение."
                )

        # Проверка частоты выполнения привычки
        frequency = habit.get("frequency", 1)
        if frequency < 1 or frequency > 7:
            raise ValidationError(
                "Периодичность выполнения привычки должна быть не реже 1 раза в 7 дней."
            )

    def create(self, request, *args, **kwargs):
        # Ваши дополнительные проверки/логику могут быть добавлены здесь, если необходимо
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Ваши дополнительные проверки/логику могут быть добавлены здесь, если необходимо
        return super().update(request, *args, **kwargs)
