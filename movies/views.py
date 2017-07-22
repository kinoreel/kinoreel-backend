from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import mixins, viewsets

from movies import models, serializers
import random

class MovieViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    serializer_class = serializers.MovieSerializer
    """
    Main class for all the api pages, self generating url if list_route is used.
    """

    def get_queryset(self):
        """
        Root entry point that returns all movies in the database
        :return: Serialized version of the Movies objects
        """
        return models.Movies.objects.all()

    @list_route(permission_classes=[],
                methods=['GET'])
    def random_movie(self, request, from_year=None, to_year=None, genre=None, language=None):
        qs = models.Movies.objects
        if language:
            qs = qs.filter(orig_language=language)
        if genre:
            genre_qs = models.Movies2Genres.objects.filter(imdb_id__in=qs.values_list('imdb_id', flat=True))
            genre_qs = genre_qs.filter(genre=genre)
            qs = qs.filter(imdb_id__in=genre_qs.values_list('imdb_id', flat=True))
        random_movie = qs.all()[int(random.random()*qs.all().count())]
        data = self.serializer_class(random_movie, many=False).data
        return Response(data)
