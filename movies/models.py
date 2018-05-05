from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Errored(models.Model):
    imdb_id = models.CharField(primary_key=True, max_length=10)
    error_message = models.CharField(max_length=4000)
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'errored'


class Genres(models.Model):
    genre = models.CharField(primary_key=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'genres'


class Iso2Language(models.Model):
    iso3166 = models.CharField(primary_key=True, max_length=2)
    language = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'iso2language'


class Language(models.Model):
    language = models.CharField(primary_key=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'language'


class Movies(models.Model):
    imdb_id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=1000)
    runtime = models.IntegerField()
    rated = models.CharField(max_length=15)
    released = models.DateField()
    plot = models.TextField()
    orig_language = models.CharField(max_length=1000)
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'movies'

    def __str__(self):
        return self.title

class PersonRoles(models.Model):
    role = models.CharField(primary_key=True, max_length=250)
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'person_roles'

    def __str__(self):
        return self.role


class Persons(models.Model):
    person_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=250)
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'persons'


class Movies2Persons(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, primary_key=True, related_name='movie_persons')
    person = models.ForeignKey(Persons, models.DO_NOTHING, related_name='person_movies')
    role = models.CharField(max_length=100)
    cast_order = models.IntegerField(blank=True, null=True)
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'movies2persons'
        unique_together = (('imdb', 'person', 'role'),)

    def __str__(self):
        return self.imdb_id


class Companies(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'companies'


class CompanyRoles(models.Model):
    role = models.CharField(primary_key=True, max_length=250)
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'company_roles'


class Movies2Companies(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING)
    company = models.ForeignKey(Companies, models.DO_NOTHING)
    role = models.ForeignKey(CompanyRoles, models.DO_NOTHING)
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'movies2companies'
        unique_together = (('imdb', 'company', 'role'),)


class Movies2Genres(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, related_name='genres', primary_key=True)
    genre = models.CharField(max_length=250)
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'movies2genres'
        unique_together = (('imdb', 'genre'),)


class Movies2Keywords(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, primary_key=True)
    keyword = models.CharField(max_length=250)
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'movies2keywords'
        unique_together = (('imdb', 'keyword'),)


class Movies2Numbers(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, primary_key=True)
    type = models.CharField(max_length=250)
    value = models.IntegerField()
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'movies2numbers'
        unique_together = (('imdb', 'type'),)


class Movies2Ratings(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, related_name='ratings', primary_key=True)
    source = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'movies2ratings'
        unique_together = (('imdb', 'source'),)


class Movies2KinoRatings(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, related_name='kinoratings', primary_key=True)
    rating = models.IntegerField()
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'kino_ratings'


class Movies2Streams(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, related_name='streams', primary_key=True)
    source = models.CharField(max_length=400)
    url = models.CharField(max_length=1000)
    currency = models.CharField(max_length=1)
    price = models.FloatField()
    format = models.CharField(max_length=30)
    purchase_type = models.CharField(max_length=30)
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'movies2streams'
        unique_together = (('imdb', 'source', 'url', 'format', 'purchase_type'),)


class Movies2Trailers(models.Model):
    imdb = models.OneToOneField(Movies, models.DO_NOTHING, related_name='trailer', primary_key=True)
    video_id = models.CharField(max_length=400)
    title = models.CharField(max_length=400)
    channel_id = models.CharField(max_length=400)
    channel_title = models.CharField(max_length=400)
    definition = models.CharField(max_length=2)
    duration = models.IntegerField()
    view_count = models.IntegerField(blank=True, null=True)
    like_count = models.IntegerField(blank=True, null=True)
    dislike_count = models.IntegerField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)
    published_at = models.DateField()
    tstamp = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'movies2trailers'

    def __str__(self):
        return self.video_id
