from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class IndexViewTestCase(TestCase):
    def test_index_view(self):
        path = reverse('myapp:index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'myapp/index.html')





