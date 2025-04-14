from django.db import models
from users.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255) # Действие
    is_pleasant = models.BooleanField(default=False) # Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки.
    related_habit = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='related_to') # Связанная привычка — привычка, которая связана с другой привычкой,
                                   # важно указывать для полезных привычек, но не для приятных.
    frequency = models.PositiveIntegerField(default=1)  # Периодичность в днях
    reward = models.TextField() # Вознаграждение
    duration = models.PositiveIntegerField(help_text="Время на выполнение в минутах")
    is_public = models.BooleanField(default=False)  # Признак публичности

    def __str__(self):
        return f'{self.action} by {self.user.username}'

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ['time']