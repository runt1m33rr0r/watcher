from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)


class ClassifierCreationDate(models.Model):
    date = models.DateTimeField(auto_now=True)


class SettingsCreationDate(models.Model):
    date = models.DateTimeField(auto_now=True)


class Settings(models.Model):
    detection_sensitivity = models.FloatField(default=0.5, validators=[MinValueValidator(0), MaxValueValidator(1)])
    downscale_level = models.IntegerField(default=2, validators=[MinValueValidator(0), MaxValueValidator(10)])
    alert_timeout = models.IntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(60)])
    camera_update_timeout = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(60)])
    camera_check_timeout = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(60)])
    model_training_timeout = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(60)])