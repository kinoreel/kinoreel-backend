from __future__ import unicode_literals

from django.db import models


class Awards(models.Model):
    imdb_event_id = models.CharField(primary_key=True, max_length=10)
    award = models.CharField(max_length=10)
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'awards'
        unique_together = (('imdb_event_id', 'award'),)


class Companies(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    founded = models.DateField(blank=True, null=True)
    dead = models.DateField(blank=True, null=True)
    country = models.ForeignKey('CountryCodes', models.DO_NOTHING, db_column='country', blank=True, null=True)
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'companies'


class CompanyRoles(models.Model):
    role = models.CharField(primary_key=True, max_length=250)
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'company_roles'


class CountryCodes(models.Model):
    country_code = models.CharField(primary_key=True, max_length=3)
    country = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'country_codes'


class Festivals(models.Model):
    imdb_event_id = models.CharField(primary_key=True, max_length=9)
    name = models.CharField(unique=True, max_length=1000)
    location = models.CharField(max_length=100)
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'festivals'


class Movies(models.Model):
    imdb_id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=1000)
    runtime = models.CharField(max_length=100)
    rated = models.CharField(max_length=15)
    released = models.CharField(max_length=15)
    orig_language = models.CharField(max_length=1000)
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'movies'


class Movies2Awards(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING)
    imdb_event = models.ForeignKey(Awards, models.DO_NOTHING)
    award = models.CharField(max_length=10)
    position = models.CharField(max_length=1, blank=True, null=True)
    year = models.DateField()
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'movies2awards'
        unique_together = (('imdb', 'award', 'year'),)


class Movies2Companies(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING)
    company = models.ForeignKey(Companies, models.DO_NOTHING, blank=True, null=True)
    role = models.CharField(max_length=250)
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'movies2companies'
        unique_together = (('imdb', 'company', 'role'),)


class Movies2Genres(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, primary_key=True)
    genre = models.CharField(max_length=250)
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'movies2genres'
        unique_together = (('imdb', 'genre'),)


class Movies2Keywords(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, primary_key=True)
    keyword = models.CharField(max_length=250)
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'movies2keywords'
        unique_together = (('imdb', 'keyword'),)


class Movies2Numbers(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, primary_key=True)
    type = models.CharField(max_length=250)
    value = models.FloatField()
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'movies2numbers'
        unique_together = (('imdb', 'type'),)


class Movies2Persons(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, primary_key=True)
    person = models.ForeignKey('Persons', models.DO_NOTHING)
    role = models.CharField(max_length=250)
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'movies2persons'
        unique_together = (('imdb', 'person', 'role'),)


class Movies2Posters(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, primary_key=True)
    url = models.CharField(unique=True, max_length=100)
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'movies2posters'


class Movies2Ratings(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, primary_key=True)
    source = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'movies2ratings'
        unique_together = (('imdb', 'source'),)


class Movies2Stats(models.Model):
    imdb_id = models.CharField(primary_key=True, max_length=10)
    tmdb_vote_average = models.FloatField(blank=True, null=True)
    tmdb_vote_count = models.FloatField(blank=True, null=True)
    imdb_votes = models.FloatField(blank=True, null=True)
    youtube_likes = models.FloatField(blank=True, null=True)
    youtube_dislikes = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies2stats'


class Movies2Streams(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, blank=True, null=True)
    source = models.CharField(max_length=400, blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)
    currency = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    format = models.CharField(max_length=30, blank=True, null=True)
    purchase_type = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies2streams'
        unique_together = (('imdb', 'source', 'url', 'format', 'purchase_type'),)


class Movies2Trailers(models.Model):
    imdb = models.ForeignKey(Movies, models.DO_NOTHING, primary_key=True)
    url = models.CharField(max_length=400)
    tstamp = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies2trailers'
        unique_together = (('imdb', 'url'),)


class PersonRoles(models.Model):
    role = models.CharField(primary_key=True, max_length=250)
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'person_roles'


class Persons(models.Model):
    person_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=250)
    dob = models.DateField(blank=True, null=True)
    dead = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    nationality = models.CharField(max_length=3, blank=True, null=True)
    tstamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'persons'