from django.test import TestCase

from rest_framework.test import APIClient

from movies.test import factories


class MovieViewSetTestCase(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.movies = factories.MoviesFactory.create()

    def test_entry(self):

        response = self.api.get('/movies/').json()
        self.assertListEqual(response,
                             [{'rated': 'For None', 'released': '1991-04-20', 'title': 'The ultimate hippie movies',
                              'runtime': '1337', 'imdb_id': 'tt1111111', 'orig_language': 'en'},])

    def test_random_movie_language(self):
        response = self.api.get('/random_movie/', {'language': 'en'}).json()
