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

    @list_route(permission_classes=[],
                methods=['GET'])
    def hello_world(self, request):
        """
        Just a test
        :param request: Request data from the api call
        :return: HTML Response
        """
        return Response({'messages': models.Movies.objects.all()[0].title}, status=200)
