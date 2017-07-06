from __future__ import unicode_literals
from django.utils import timezone

from django.db import models

# Create your models here.
class Movie(models.Model):
    imdb_id = models.CharField(max_length=10, primary_key=True, null=False)
    title = models.CharField(max_length=1000, null=False)
    runtime = models.CharField(max_length=100, null=False)
    rated = models.CharField(max_length=15, null=False)
    released = models.CharField(max_length=15, null=False)
    orig_language = models.CharField(max_length=1000, null=False)
    tstamp = models.DateTimeField(default=timezone.now)


class Companies(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000, null=False, unique=True)
    tstamp = models.DateTimeField(default=timezone.now)


class Persons(models.Model):
    person_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=1000, null=False, unique=True)
    tstamp = models.DateTimeField(default=timezone.now)


class Festivals(models.Model):
    imdb_event_id = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=1000, null=False)
    location = models.CharField(max_length=1000, null=False)
    tstamp = models.DateTimeField(default=timezone.now)


class Person_Roles(models.Model):
    role = models.CharField(max_length=1000, primary_key=True)
    tstamp = models.DateTimeField(default=timezone.now)


class Company_Roles(models.Model):
    role = models.CharField(max_length=1000, primary_key=True)
    tstamp = models.DateTimeField(default=timezone.now)


class Movie2Awards(models.Model):
    imdb_id = models.ForeignKey(Movie)
    imdb_event_id = models.ForeignKey(Festivals)
    award = models.CharField(max_length=10, null=False)
    position = models.CharField(max_length=1, null=False, choices=[('Y', 'yes'), ('N', 'No')])
    year = models.CharField(max_length=4, null=False)
    tstamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('imdb_id', 'year', 'award')


class Movies2Companies(models.Model):
    imdb_id = models.ForeignKey(Movie)
    company_id = models.ForeignKey(Companies)
    role = models.CharField(max_length=100, null=False)
    tstamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('imdb_id', 'company_id', 'role')


class Movies2Genres(models.Model):
    imdb_id = models.ForeignKey(Movie)
    genre = models.CharField(max_length=250, primary_key=True)
    tstamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('imdb_id', 'genre')


class Movies2Keywords(models.Model):
    imdb_id = models.ForeignKey(Movie)
    keyword = models.CharField(max_length=250)
    tstamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('imdb_id', 'keyword')


class Movies2Numbers(models.Model):
    imdb_id = models.ForeignKey(Movie)
    type = models.CharField(max_length=250)
    value = models.BigIntegerField(null=False)
    tstamp = models.DateTimeField(default=timezone.now)


class Movies2Persons(models.Model):
    imdb_id = models.ForeignKey(Movie)
    person_id = models.ForeignKey(Persons)
    role = models.ForeignKey(Person_Roles)
    tstamp = models.DateTimeField(default=timezone.now)

    class Meta:
         unique_together = ('imdb_id', 'person_id', 'role')


class Movies2Posters(models.Model):
    imdb_id = models.ForeignKey(Movie)
    url = models.CharField(max_length=1000)
    tstamp = models.DateTimeField(default=timezone.now)

    class Meta:
         unique_together = ('imdb_id', 'url')


class Movies2Ratings(models.Model):
    imdb_id = models.ForeignKey(Movie)
    source = models.CharField(max_length=250)
    rating = models.CharField(max_length=100, null=False)
    tstamp = models.DateTimeField(default=timezone.now)

    class Meta:
         unique_together = ('imdb_id', 'source')


class Movies2Stats(models.Model):
    imdb_id = models.OneToOneField(Movie)
    tmdb_vote_average = models.BigIntegerField()
    tmdb_vote_count = models.BigIntegerField()
    imdb_votes = models.BigIntegerField()
    youtube_likes = models.BigIntegerField()
    youtube_dislikes= models.BigIntegerField()
    tstamp = models.DateTimeField(default=timezone.now)


class Movies2Streams(models.Model):
    imdb_id = models.ForeignKey(Movie)
    source = models.CharField(max_length=250, null=False)
    url = models.CharField(max_length=1000, null=False)
    currency = models.CharField(max_length=1, null=False, choices=[('£', 'Pound'), ('$', 'Dollar')])
    price = models.CharField(max_length=250)
    format = models.CharField(max_length=30)
    purchase_type = models.CharField(max_length=30)
    tstamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together=('imdb_id', 'source', 'url', 'format', 'purchase_type')


class Movies2Trailers(models.Model):
    imdb_id = models.ForeignKey(Movie)
    url = models.CharField(max_length=1000)
    tstamp = models.DateTimeField(default=timezone.now)

    class Meta:
         unique_together = ('imdb_id', 'url')
