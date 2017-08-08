import factory

from movies import models


class MoviesFactory(factory.DjangoModelFactory):
    """ Factory for the Books model. """
    class Meta:
        model = models.Movies

    imdb_id = 'tt4285496'
    title = 'Embrace of the Serpent'
    runtime = '125'
    rated = '12'
    released = '2015-05-25'
    orig_language = 'es'


class Movies2GenresFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Movies2Genres

    imdb_id = 'tt4285496'
    genre = 'Action'
    tstamp = '2015-05-25'


