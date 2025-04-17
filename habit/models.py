from django.db import models
from rest_framework.exceptions import ValidationError

from users.models import User


class RelatedHabit(models.Model):
    habit = models.CharField(
        max_length=255, verbose_name="Связанная привычка", null=True, blank=True
    )


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(
        max_length=255, verbose_name="Место выполнения", null=True, blank=True
    )
    time = models.TimeField(
        verbose_name="Во сколько выполнять привычку?", null=True, blank=True
    )
    action = models.CharField(
        max_length=255, verbose_name="Привычка", null=True, blank=True
    )  # Действие
    is_pleasant = models.BooleanField(
        default=False, verbose_name="Приятная привычка", null=True, blank=True
    )  # Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки.
    related_habit = models.ForeignKey(
        RelatedHabit,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="related_to",
    )  # Связанная привычка — привычка, которая связана с другой привычкой,
    # важно указывать для полезных привычек, но не для приятных.
    frequency = models.PositiveIntegerField(
        default=1, verbose_name="Периодичность", null=True, blank=True
    )  # Периодичность в днях
    reward = models.TextField(verbose_name="Вознаграждение")  # Вознаграждение
    duration = models.PositiveIntegerField(
        help_text="Время на выполнение в минутах", null=True, blank=True
    )
    is_public = models.BooleanField(
        default=False, verbose_name="Статус публичности", null=True, blank=True
    )  # Признак публичности
    tg_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.action} by {self.user.username}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["time"]

    def clean(self):
        """Метод для валидации на стадии создания модели.
        Должно быть заполнено только одно из полей(Приятная привычка or Вознаграждение)"""
        super().clean()
        # Проверяем, заполнено ли одно из двух полей
        if not (self.is_pleasant or self.reward):
            raise ValidationError(
                "Должно быть заполнено хотя бы одно из полей: field_one или field_two."
            )
        if self.is_pleasant and self.reward:
            raise ValidationError(
                "Заполните только одно поле: field_one или field_two."
            )
