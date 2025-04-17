from django.urls import reverse
from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreateViewTests(TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("users:register")  # Здесь указывайте правильный путь
        self.valid_data = {
            "email": "test@example.com",
            "password1": "Password123!",
            "password2": "Password123!",
        }

    def test_user_creation_success(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект
        self.assertTrue(User.objects.filter(email="test@example.com").exists())
        user = User.objects.get(email="test@example.com")
        self.assertFalse(user.is_active)
        self.assertIsNotNone(user.token)

        # Проверяем, что было отправлено одно письмо
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Подтвердите email адрес")
        self.assertIn(user.token, mail.outbox[0].body)

    def test_user_creation_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data["password2"] = "DifferentPassword123!"

        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Все еще на той же странице
        # self.assertFormError(response, 'form', 'password2', 'Пароли не совпадают.')  # Сообщение об ошибке

    def test_user_creation_email_already_exists(self):
        User.objects.create(email="test@example.com", password="Password123!")

        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(
            response.status_code, 200
        )  # Ожидаем, что форма будет отрисована снова
        # self.assertFormError(response, 'form', 'email',
        #                      'Пользователь с таким email уже существует.')  # Сообщение об ошибке

    def test_email_sent_with_correct_url(self):
        # response = self.client.post(self.url, self.valid_data)
        user = User.objects.get(email="test@example.com")

        # Проверяем, что было отправлено одно письмо
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Подтвердите email адрес")

        # Проверяем правильность URL в теле письма
        host = "testserver"  # Получить обработанный хост
        url = f"http://{host}/email-confirm/{user.token}/"
        self.assertIn(url, mail.outbox[0].body[73:])
