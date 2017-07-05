from __future__ import unicode_literals
from django.utils import timezone

from django.db import models

# Create your models here.
class Movie(models.Model):
    imdb_id = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=1000, null=False)
    runtime = models.CharField(max_length=100, null=False)
    rated = models.CharField(max_length=15, null=False)
    released = models.CharField(max_length=15, null=False)
    orig_language = models.CharField(max_length=1000, null=False)
    tstamp = models.DateTimeField(default=timezone.now)