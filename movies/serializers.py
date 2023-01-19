from rest_framework import serializers

from movies import models


class KinoRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movies2KinoRatings
        fields = (
            'rating'
        )


class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movies2Ratings
        fields = (
            'source',
            'rating'
        )


class StreamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movies2Streams
        fields = (
            'source',
            'url',
            'currency',
            'price',
            'purchase_type',
        )


class PersonsSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='person.fullname')

    class Meta:
       model = models.Movies2Persons
       fields = ('imdb_id', 'fullname', 'role',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Movies2Genres
        fields = ('genre', )


class MovieSerializer(serializers.ModelSerializer):
    trailer = serializers.StringRelatedField(many=False)
    persons = PersonsSerializer(source='movie_persons', many=True)
    ratings = RatingsSerializer(many=True)
    kinoratings = KinoRatingsSerializer(many=True)
    genres = GenreSerializer(many=True)
    streams = StreamsSerializer(many=True)

    class Meta:
        model = models.Movies
        fields = (
            'imdb_id',
            'title',
            'plot',
            'runtime',
            'rated',
            'released',
            'orig_language',
            'trailer',
            'ratings',
            'kinoratings',
            'streams',
            'genres',
            'persons'
        )

