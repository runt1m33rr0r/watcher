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
from ..forms import AlertForm


@csrf_exempt
def register_camera(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        city = City.objects.filter(name=data.get('city'))

        if city.exists():
            city = city.first()
        else:
            city = CitySerializer(data={ 'name': data.get('city') })

            if city.is_valid():
                city = city.save()
            else:
                return JsonResponse(city.errors, status=status.HTTP_400_BAD_REQUEST)

        camera = CameraSerializer(data=data)

        if camera.is_valid():
            saved = camera.save()
            city.cameras.add(saved)

            return JsonResponse(camera.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(camera.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def get_settings_date(request):
    if request.method == 'GET':
        Settings.objects.get_or_create()
        date = SettingsCreationDate.objects.get_or_create()[0].date
        
        return JsonResponse({ 'success': True, 'date': date })


@csrf_exempt
def get_settings(request):
    if request.method == 'GET':
        settings = Settings.objects.get_or_create()[0]
        res = {
            'success': True,
            'detection_sensitivity': settings.detection_sensitivity,
            'downscale_level': settings.downscale_level,
            'alert_timeout': settings.alert_timeout,
            'camera_update_timeout': settings.camera_update_timeout,
        }
        
        return JsonResponse(res)


@csrf_exempt
def alert(request, person_id=None):
    if request.method == 'POST':
        alert_form = AlertForm(request.POST, request.FILES)

        if alert_form.is_valid():
            data = alert_form.cleaned_data
            person_name = data['name']
            city_name = data['city']
            image_file = data['image']

            try:
                person = Person.objects.get(name=person_name)
            except Person.DoesNotExist:
                return JsonResponse({ 'success': True, 'message': 'Person does not exist!' })
            
            try:
                city = City.objects.get(name=city_name)
            except City.DoesNotExist:
                return JsonResponse({ 'success': True, 'message': 'Person does not exist!' }) 

            image = Image(image_file=image_file)
            set_save_location(f'{DETECTIONS_FOLDER_NAME}')
            image.save()

            detection = Detection(city=city, person=person, image=image)
            detection.save()
            detected(person_name, city_name, f'detections/{person.id}')

            return JsonResponse({ 'success': True })
        else:
            return JsonResponse({ 'error': True })


@csrf_exempt
def get_classifier_file(request):
    if request.method == 'GET':
        return serve(request, os.path.basename(classifier_path), os.path.dirname(classifier_path))


@csrf_exempt
def get_classifier_date(request):
    if request.method == 'GET':
        if ClassifierCreationDate.objects.filter().exists():
            date = ClassifierCreationDate.objects.get()

            return JsonResponse({ 'success': True, 'date': date.date })
        else:
            return JsonResponse({ 'error': True, 'date': None })