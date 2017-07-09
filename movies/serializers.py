from rest_framework import serializers

from movies import models


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movies
        fields = (
            'imdb_id',
            'title',
            'runtime',
            'rated',
            'released',
            'orig_language'
        )
