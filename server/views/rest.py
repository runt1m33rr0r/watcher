import os
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.static import serve
from ..ai.classifier import classifier_path
from ..serializers import CameraSerializer, CitySerializer
from ..models import City, Settings, SettingsCreationDate, Detection, Image, Person, ClassifierCreationDate
from ..utils.storage import set_save_location, DETECTIONS_FOLDER_NAME
from ..utils.detections_watcher import detected


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


@csrf_exempt
def alert(request, person_id=None):
    if request.method == 'POST':
        person_name = request.POST['name']
        person = Person.objects.get(name=person_name)
        city_name = request.POST['city']
        city = City.objects.get(name=city_name)
        image_file = request.FILES['image']
        image = Image(image_file=image_file)

        set_save_location(f'{DETECTIONS_FOLDER_NAME}')
        image.save()

        detection = Detection(city=city, person=person, image=image)
        detection.save()

        detected(person_name, city_name, f'detections/{person.id}')

        return JsonResponse({ 'success': True })


@csrf_exempt
def get_classifier_file(request):
    if request.method == 'GET':
        return serve(request, os.path.basename(classifier_path), os.path.dirname(classifier_path))


@csrf_exempt
def get_classifier_date(request):
    if request.method == 'GET':
        if ClassifierCreationDate.objects.filter().exists():
            date = ClassifierCreationDate.objects.get()

            return JsonResponse({ 'date': date.date })
        else:
            return JsonResponse({ 'date': None })