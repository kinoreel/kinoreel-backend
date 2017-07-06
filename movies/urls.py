from django.conf.urls import include, url
from rest_framework_nested import routers

from movies import views


movie_router = routers.SimpleRouter()
movie_router.register(r'movies', views.MovieViewSet, base_name='movies')

urlpatterns = [
    url(r'^', include(movie_router.urls))
]
