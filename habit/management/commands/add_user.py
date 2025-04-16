from django.core.management.base import BaseCommand
from users.models import User# Импортируйте вашу модель

class Command(BaseCommand):
    help = 'Добавляет данные в таблицу MyModel'

    def handle(self, *args, **kwargs):
        # Пример добавления одного объекта
        my_instance = User(email='test3@gmail.com', is_active=True, password='1234qwertyu')
        my_instance.save()
        self.stdout.write(self.style.SUCCESS('Данные успешно добавлены!'))

