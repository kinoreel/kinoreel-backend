import datetime
from random import randint
from django.db.models import F

from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from movies import models, serializers


class RoleViewSet(viewsets.ViewSet):

    @action(detail=False)
    def directors(self, request):
        qs = models.Movies2Persons.objects.filter(role="director").values_list("person__fullname", flat=True)
        return Response(qs)

    @action(detail=False)
    def dops(self, request):
        qs = models.Movies2Persons.objects.filter(role="director of photography").values_list("person__fullname", flat=True)
        return Response(qs)

    @action(detail=False)
    def editors(self, request):
        qs = models.Movies2Persons.objects.filter(role="editor").values_list("person__fullname", flat=True)
        return Response(qs)

    @action(detail=False)
    def screenwriters(self, request):
        qs = models.Movies2Persons.objects.filter(role="screenplay").values_list("person__fullname", flat=True)
        return Response(qs)


class KinoRatingViewSet(viewsets.ViewSet):

    @action(detail=False)
    def kino(self, request):
        imdb_id = request.GET.get('imdb_id')
        rating = request.GET.get('rating')
        print(imdb_id)
        print(rating)
        m = models.Movies2KinoRatings(imdb_id=imdb_id, rating=rating)
        m.save()
        return Response({"result": "Successfully saved"})


class MoviesViewSet(viewsets.ViewSet):
    serializer_class = serializers.MovieSerializer

    @action(detail=False)
    def person(self, request):
        person = request.GET.get('person')
        role = request.GET.get('role')
        movie = models.Movies.objects.filter(movies2persons__person=person)
        data = self.serializer_class(movie, many=False).data
        return Response(data)

    @action(detail=False)
    def imdb_id(self, request):
        imdb_id = request.GET.get('imdb_id')
        movie = models.Movies.objects.get(imdb_id=imdb_id)
        data = self.serializer_class(movie, many=False).data
        return Response(data)

    @action(detail=False)
    def titles(self, request):
        qs = self.filtered_queryset(request).values('title', 'imdb_id')
        return Response(qs)

    @action(detail=False)
    def random(self, request):
        qs = self.filtered_queryset(request)

        # If the filters are too strict and no film can be found, return 'No data found'
        if qs.count() == 0:
            return Response('No data found')

        seen = request.GET.get('seen')
        if seen:
            seen_films = seen.split(",")
            if qs.count() <= len(seen_films):
                next_imdb_id = seen_films[0]
                print(next_imdb_id)
                qs = qs.get(imdb_id=next_imdb_id)
                data = self.serializer_class(qs, many=False).data
                return Response(data)
            else:
                qs = qs.exclude(imdb_id__in=seen_films)

        # NOTE: Apparently method faster than qs[50].order_by('?').first()
        # - https://stackoverflow.com/questions/962619
        random_index = randint(0, min(50, qs.count() - 1))
        qs = qs[random_index]

        data = self.serializer_class(qs, many=False).data

        return Response(data)

    def filtered_queryset(self, request):
        qs = models.Movies.objects.all()
        # Filtering on language

        if request.GET.get('imdb_id'):
            return qs.get(imdb_id=request.GET['imdb_id'])

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
            qs = qs.filter(genres__genre__in=genres) \
                .annotate(num_genres=Count('genres')).filter(num_genres=len(genres))

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

        if request.GET.get('unrated'):
            inner_qs = models.Movies2KinoRatings.objects.all()
            qs = qs.exclude(imdb_id__in=inner_qs.values_list('imdb_id'))
        else:
            inner_qs = models.Movies2KinoRatings.objects.filter(rating__gte=2)
            qs = qs.filter(imdb_id__in=inner_qs.values_list('imdb_id'))
            qs = qs.order_by(F('kinoratings').desc(nulls_last=True))

        return qs
