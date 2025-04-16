from celery import shared_task
from datetime import datetime
from django.utils import timezone
from habit.models import Habit  # Импортируйте вашу модель
from habit.services import send_message  # Импортируйте вашу функцию отправки сообщения

@shared_task
def check_and_send_messages():
    now = timezone.now()
    items = Habit.objects.filter(time=now)  # Предположим, у вас есть поле message_sent
    print(now)

    for item in items:
        message = f'Пора выполнить {item.action} в {item.place} в {item.time}'
        send_message(item.tg_id, message)  # Ваш вызов функции отправки сообщения
        item.message_sent = True  # Устанавливайте флаг, чтобы не отправлять сообщение повторно
        item.save()

