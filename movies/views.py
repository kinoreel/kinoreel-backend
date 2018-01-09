from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import mixins, viewsets

from movies import models, serializers
import random
import datetime

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

    @list_route(permission_classes=[], methods=['GET'])
    def random_movie(self, request):
        qs = models.Movies.objects
        if request.GET.get('source'):
            streams_qs = models.Movies2Streams.objects.filter(imdb_id__in=qs.values_list('imdb_id', flat=True))
            streams_qs = streams_qs.filter(source__iexact=request.GET['source'])
            qs = qs.filter(imdb_id__in=streams_qs.values_list('imdb_id', flat=True))
        if request.GET.get('imdb_min'):
            imdb_min_qs = models.Movies2Ratings.objects.filter(imdb_id__in=qs.values_list('imdb_id', flat=True),
                                                               source='imdb')
            imdb_min_qs = imdb_min_qs.filter(rating__gte=float(request.GET.get('imdb_min')))
            qs = qs.filter(imdb_id__in=imdb_min_qs.values_list('imdb_id', flat=True))
        if request.GET.get('imdb_max'):
            imdb_max_qs = models.Movies2Ratings.objects.filter(imdb_id__in=qs.values_list('imdb_id', flat=True),
                                                               source='imdb')
            imdb_max_qs = imdb_max_qs.filter(rating__lte=float(request.GET.get('imdb_max')))
            qs = qs.filter(imdb_id__in=imdb_max_qs.values_list('imdb_id', flat=True))
        if request.GET.get('rotten_min'):
            rotten_min_qs = models.Movies2Ratings.objects.filter(imdb_id__in=qs.values_list('imdb_id', flat=True),
                                                                 source='rotten tomatoes')
            rotten_min_qs = rotten_min_qs.filter(rating__gte=float(request.GET.get('rotten_min')))
            qs = qs.filter(imdb_id__in=rotten_min_qs.values_list('imdb_id', flat=True))
        if request.GET.get('rotten_max'):
            rotten_max_qs = models.Movies2Ratings.objects.filter(imdb_id__in=qs.values_list('imdb_id', flat=True),
                                                                 source='rotten tomatoes')
            rotten_max_qs = rotten_max_qs.filter(rating__lte=float(request.GET.get('rotten_max')))
            qs = qs.filter(imdb_id__in=rotten_max_qs.values_list('imdb_id', flat=True))
        if request.GET.get('language'):
            qs = qs.filter(orig_language=request.GET['language'])
        if request.GET.get('genre'):
            genre_qs = models.Movies2Genres.objects.filter(imdb_id__in=qs.values_list('imdb_id', flat=True))
            genre_qs = genre_qs.filter(genre=request.GET['genre'])
            qs = qs.filter(imdb_id__in=genre_qs.values_list('imdb_id', flat=True))
        if request.GET.get('from_year'):
            qs = qs.filter(released__gte=datetime.datetime(request.GET['from_year'], 1, 1))
        if request.GET.get('to_year'):
            qs = qs.filter(released__lte=datetime.datetime(request.GET['to_year'], 12, 31))
        data = {}
        if qs.all().count():
            random_movie = qs.all()[int(random.random()*qs.all().count())]
            data = self.serializer_class(random_movie, many=False).data
        return Response(data)
