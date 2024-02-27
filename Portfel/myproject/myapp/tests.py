from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class IndexViewTestCase(TestCase):
    def test_index_view(self):
        path = reverse('myapp:index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'myapp/index.html')



from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import HistoryModel, ActiveModel

class BreafceseListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.active = ActiveModel.objects.create(active_name='Test Active', now_price=100)
        self.history = HistoryModel.objects.create(user_id=self.user, active_id=self.active, price=100, count=10)
        self.url = reverse('brefcese')  # Предполагается, что у вас есть URL-маршрут с именем 'brefcese'

    def test_breafcese_list_view_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/brefcese.html')

    def test_breafcese_list_view_returns_correct_queryset(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Active')
        # Добавьте дополнительные проверки, если необходимо

    def test_breafcese_list_view_requires_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/accounts/login/?next=' + self.url)

# Добавьте дополнительные тесты, если необходимо

