from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.


class Movies(models.Model):
    id = models.UUIDField(primary_key=True, editable=True)
    title = models.CharField(max_length=500)
    description = models.TextField()
    genres = models.CharField(max_length=500)


class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movies, blank=True)
