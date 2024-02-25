from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse


class UsersLoginTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser',
                                                         password='123')  # Имитация созданного пользователя

    def test_login_get(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, HTTPStatus.OK)  # Проверка на get запрос по URL и его отображения

    def test_login_post(self):
        credentials = {                               # Имитация ввода данных
            'username': 'testuser',
            'password': '123'
        }
        response = self.client.post('/users/login/', credentials)   #
        self.assertRedirects(response, reverse('myapp:index'))

    def test_login_with_wrong_credentials(self):
        # Отправляем POST-запрос с неправильными учетными данными
        response = self.client.post(reverse('users:login'), {
            'username': 'wronguser',
            'password': 'wrongpass'
        })

        self.assertEqual(response.status_code, HTTPStatus.OK)


