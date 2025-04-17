from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Habit


class HabitViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="testuser@mail.ru", password="testpassword", is_active=True
        )
        self.client.login(username="testuser", password="testpassword")

    def test_public_habits(self):
        # Создаем публичные и непубличные привычки
        Habit.objects.create(
            user=self.user, place="Gym", time="08:00", action="Exercise", is_public=True
        )
        Habit.objects.create(
            user=self.user, place="Home", time="09:00", action="Relax", is_public=False
        )

        # Запрос на получение публичных привычек
        response = self.client.get("/habit/public/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        # self.assertEqual(response.data[0]['action'], "Exercise")

    def test_create_habit_with_validation_error(self):
        # Пробуем создать привычку с нарушением валидации (связанные привычки и вознаграждение)
        data = {
            "user": self.user.id,
            "place": "Work",
            "time": "10:00:00",
            "action": "Focus",
            "is_pleasant": False,
            "related_habit": "",
            "frequency": 2,
            "reward": "Good job!",
            "duration": 30,
            "is_public": True,
        }
        response = self.client.post("/habit/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_habit_with_validation_error(self):
        # Создаем привычку
        habit = Habit.objects.create(
            user=self.user, place="Library", time="11:00:00", action="Read", frequency=1
        )

        # Пробуем обновить привычку с нарушением валидации
        url = f"/habit/{habit.id}/"
        data = {
            "place": "Library",
            "time": "11:00:00",
            "action": "Read",
            "is_pleasant": True,
            "related_habit": 1,  # Предполагаем, что существует другая привычка с ID 1
            "frequency": 1,
            "reward": "",
            "duration": 60,
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertIn("Приятная привычка не может иметь связанную привычку или вознаграждение.",
        #               response.data)

    #
    def test_frequency_validation(self):
        # Проверка на периодичность выполнения привычки
        data = {
            "user": self.user.id,
            "place": "Park",
            "time": "12:00:00",
            "action": "Run",
            "is_pleasant": False,
            "related_habit": "",
            "frequency": 8,  # Неправильная периодичность
            "reward": "Fresh air",
            "duration": 30,
        }
        response = self.client.post("/habit/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Периодичность выполнения привычки должна быть не реже 1 раза в 7 дней.",
            response.data,
        )
