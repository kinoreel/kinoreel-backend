from rest_framework import serializers

from movies import models


class TrailersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movies2Trailers
        fields = ('video_id',)


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
            'purchase_type'
        )


class MovieSerializer(serializers.ModelSerializer):
    trailers = TrailersSerializer(many=True)
    ratings = RatingsSerializer(many=True)
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
            'trailers',
            'ratings',
            'streams'
        )
