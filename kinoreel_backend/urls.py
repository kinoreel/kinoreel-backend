from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login

from movies.urls import urlpatterns as movie_urls

urlpatterns = [
    url(r'^', include(movie_urls), name='movies'),
    url(r'^admin/', include(admin.site.urls)),
]
