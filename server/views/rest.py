from rest_framework.parsers import JSONParser
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ..serializers import CameraSerializer, CitySerializer
from ..models import City, Settings, SettingsCreationDate


@csrf_exempt
def register_camera(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        city = City.objects.filter(name=data.get('city'))

        if city.exists():
            city = city.first()
        else:
            city = CitySerializer(data={'name': data.get('city')})

            if city.is_valid():
                city = city.save()
            else:
                return JsonResponse(city.errors, status=status.HTTP_400_BAD_REQUEST)

        camera = CameraSerializer(data=data)

        if camera.is_valid():
            saved = camera.save()
            print(saved)
            city.cameras.add(saved)

            return JsonResponse(camera.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(camera.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def get_settings_date(request):
    if request.method == 'GET':
        Settings.objects.get_or_create()
        date = SettingsCreationDate.objects.get_or_create()[0].date
        
        return JsonResponse({ 'date': date })


@csrf_exempt
def get_settings(request):
    if request.method == 'GET':
        settings = Settings.objects.get_or_create()[0]
        res = {
            'detection_sensitivity': settings.detection_sensitivity,
            'downscale_level': settings.downscale_level,
            'alert_timeout': settings.alert_timeout,
            'camera_update_timeout': settings.camera_update_timeout,
        }
        
        return JsonResponse(res)