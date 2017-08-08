from django.test import TestCase
from rest_framework.test import APIClient
from movies.test import factories
import random


class MovieViewSetTestCase(TestCase):

    def setUp(self):
        self.api = APIClient()

    def test_random_movie_language(self):
        for lang in ('en', 'de', 'fr'):
            factories.MoviesFactory.create(orig_language=lang, imdb_id='tt'+str(random.choice(range(10000, 90000))))
        response = self.api.get('/movies/random_movie/?language=en').json()
        self.assertEqual(response['orig_language'], 'en')

    def test_random_movie_genre(self):
        test_data = {
            'action': 'tt111111',
            'horror': 'tt222222',
            'romance': 'tt333333'
        }
        for genre, imdb_id in test_data.items():
            factories.MoviesFactory.create(imdb_id=imdb_id)
            factories.Movies2GenresFactory.create(genre=genre, imdb_id=imdb_id)
        response = self.api.get('/movies/random_movie/?genre=horror').json()
        self.assertEqual(response['imdb_id'], 'tt222222')
