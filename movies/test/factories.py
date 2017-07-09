import factory

from movies import models


class MoviesFactory(factory.DjangoModelFactory):
    """ Factory for the Books model. """
    class Meta:
        model = models.Movies

    imdb_id = 'tt1111111'
    title = 'The ultimate hippie movies'
    runtime = '1337'
    rated = 'For None'
    released = '1991-04-20'
    orig_language = 'en'
