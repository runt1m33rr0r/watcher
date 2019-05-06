from django.db import models
from .utils.storage import decide_save_location


class Camera(models.Model):
    url = models.CharField(max_length=1000, unique=True)
    name = models.CharField(max_length=100, unique=True)


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cameras = models.ManyToManyField(Camera)


class Image(models.Model):
    image_file = models.ImageField(upload_to=decide_save_location)


class Person(models.Model):
    name = models.CharField(max_length=100, unique=True)
    images = models.ManyToManyField(Image)


class Detection(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class ClassifierCreationDate(models.Model):
    date = models.DateTimeField(auto_now=True)