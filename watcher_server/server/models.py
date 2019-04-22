from django.db import models


class Camera(models.Model):
    url = models.CharField(max_length=1000)


class City(models.Model):
    name = models.CharField(max_length=100)
    cameras = models.ManyToManyField(Camera)
