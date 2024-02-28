from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse


class IndexViewTestCase(TestCase):
    def test_index_view(self):
        path = reverse('myapp:index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'myapp/index.html')

    def test_index_conntext(self):
        path = reverse('myapp:index')
        response = self.client.get(path)

        self.assertIn('expected_key', response.context) # Проверяем, что в контексте ответа есть ожидаемый ключ 'expected_key'
        self.assertEqual(response.context['expected_key'], 'expected_value') # Проверяем, что значение по ключу 'expected_key' в контексте ответа равно 'expected_value'


