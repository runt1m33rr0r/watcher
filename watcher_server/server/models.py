from django.db import models


class Camera(models.Model):
    url = models.CharField(max_length=1000, unique=True)
    name = models.CharField(max_length=100, unique=True)


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cameras = models.ManyToManyField(Camera)


class Image(models.Model):
    image_file = models.ImageField()


class Person(models.Model):
    name = models.CharField(max_length=100)
    images = models.ManyToManyField(Image)


class Detection(models.Model):
    date = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    image = models.ImageField()