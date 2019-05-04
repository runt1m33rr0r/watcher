from django.db import models


class Camera(models.Model):
    url = models.CharField(max_length=1000, unique=True)
    name = models.CharField(max_length=100, unique=True)


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cameras = models.ManyToManyField(Camera)
