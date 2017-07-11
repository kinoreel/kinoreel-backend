from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import mixins, viewsets

from movies import models, serializers

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
