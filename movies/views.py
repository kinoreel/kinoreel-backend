import functools
import operator

from django.db.models import Q
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import mixins, viewsets

from movies import models, serializers
import datetime
from random import randint


class MovieViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    movie_serializer = serializers.MovieSerializer
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
        # Filtering on language
        if request.GET.get('language'):
            qs = qs.filter(orig_language__in=request.GET['language'].split(','))

        # Filtering on release date
        if request.GET.get('from_year'):
            qs = qs.filter(released__gte=datetime.datetime(int(request.GET['from_year']), 1, 1))
        if request.GET.get('to_year'):
            qs = qs.filter(released__lte=datetime.datetime(int(request.GET['to_year']), 12, 31))

        # Filtering on runtime
        if request.GET.get('runtime_min'):
            qs = qs.filter(runtime__gte=int(request.GET['runtime_min']))
        if request.GET.get('runtime_max'):
            qs = qs.filter(runtime__lte=int(request.GET['runtime_max']))

        # Filtering on requested streams
        if request.GET.get('streams'):
            qs = qs.filter(streams__source__in=request.GET['streams'].split(','))

        # Filtering on genre
        if request.GET.get('genres'):
            genres = request.GET['genres'].split(',')
            functools.reduce(operator.and_, (Q(genres__genre__contains=genre) for genre in genres))

        # Filtering based on ratings
        if request.GET.get('imdb_min'):
            inner_qs = models.Movies2Ratings.objects.filter(source='imdb',
                                                            rating__gte=float(request.GET['imdb_min']))
            qs = qs.filter(imdb_id__in=inner_qs.values_list('imdb_id', flat=True))
        if request.GET.get('imdb_max'):
            inner_qs = models.Movies2Ratings.objects.filter(source='imdb',
                                                            rating__lte=float(request.GET['imdb_max']))
            qs = qs.filter(imdb_id__in=inner_qs.values_list('imdb_id', flat=True))
        if request.GET.get('rotten_min'):
            inner_qs = models.Movies2Ratings.objects.filter(source='rotten tomatoes',
                                                            rating__gte=float(request.GET['rotten_min']))
            qs = qs.filter(imdb_id__in=inner_qs.values_list('imdb_id', flat=True))
        if request.GET.get('rotten_max'):
            inner_qs = models.Movies2Ratings.objects.filter(source='rotten tomatoes',
                                                            rating__lte=float(request.GET['rotten_max']))
            qs = qs.filter(imdb_id__in=inner_qs.values_list('imdb_id', flat=True))

        # If the filters are too strict and no film can be found, return 'No data found'
        if qs.count() == 0:
            return Response('No data found')

        # The length of seen films always less then 50, so
        # if the query set is greater then 50 we are safe to exclude them.
        if qs.count() > 50 and request.GET.get('seen'):
            qs = qs.exclude(imdb_id__in=request.GET.get('seen').split(','))

        # We then pick a random film from the 50 films with the highest kino rating
        qs = qs.order_by('-kinoratings__rating')

        # NOTE: Apparently method faster than qs[50].order_by('?').first()
        # - https://stackoverflow.com/questions/962619
        random_index = randint(0, min(50, qs.count() - 1))
        qs = qs[random_index]

        data = self.movie_serializer(qs, many=False).data

        return Response(data)

    @list_route(permission_classes=[], methods=['GET'])
    def imdb_id(self, request):
        qs = models.Movies.objects
        imdb_id = request.GET.get('imdb_id')
        movie = qs.get(imdb_id=imdb_id)
        data = self.movie_serializer(movie, many=False).data
        return Response(data)
