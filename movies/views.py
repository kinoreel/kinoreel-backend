from django.shortcuts import render
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import mixins, viewsets


class MovieViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    Main class for all the api pages, self generating url if list_route is used
    """
    @list_route(permission_classes=[],
                methods=['GET'])
    def hello_world(self, request):
        """
        Just a test
        :param request: Request data from the api call
        :return: HTML Response
        """
        return Response({'messages': ['Hello World']}, status=200)
