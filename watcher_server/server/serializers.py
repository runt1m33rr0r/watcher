from .models import Camera, City, Detection
from rest_framework import serializers


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ('url', 'name')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name',)


class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = ('date', 'city', 'camera', 'image')