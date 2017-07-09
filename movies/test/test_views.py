from django.test import TestCase

from rest_framework.test import APIClient

from movies.test import factories

class MovieViewSetTestCase(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.movies = factories.MoviesFactory.create()

    def test_hello_world(self):

        response = self.api.get('/movies/hello_world/').json()

        self.assertDictEqual(response, {'messages': 'Hello World'})

    def test_entry(self):

        response = self.api.get('/movies/').json()
        print(response)
