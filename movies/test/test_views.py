from django.test import TestCase

from rest_framework.test import APIClient


class MovieViewSetTestCase(TestCase):
    def setUp(self):
        self.api = APIClient()

    def test_hello_world(self):

        response = self.api.get('/movies/hello_world/').json()

        self.assertDictEqual(response, {'messages': 'Hello World'})
