import os
import io
import base64
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.static import serve
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from ..ai.classifier import classifier_path
from ..models import ClassifierCreationDate, City, Detection, Person, Camera, Image
from ..utils.storage import set_save_location, DETECTIONS_FOLDER_NAME, delete_file


def cameras(request):
    if request.method == 'GET':
        city = City.objects.first()
        camera = city.cameras.first()

        return redirect(f'/cameras/{city.id}/{camera.id}')


def city(request, city_id):
    if request.method == 'GET':
        city = City.objects.get(id=city_id)
        chosen_camera = city.cameras.first()

        return redirect(f'/cameras/{city_id}/{chosen_camera.id}')


def camera(request, city_id, camera_id):
    if request.method == 'GET':
        cities = City.objects.all()
        ctx = {}

        if cities.count() == 0:
            ctx = {  
                'cities': [], 
                'cameras': [],
                'chosen_city': None,
                'chosen_camera': None,
                'success': True, 
                'message': 'There are no cameras in the system!',
            }
        else:
            chosen_city = City.objects.get(id=city_id)
            cameras = chosen_city.cameras.all()
            camera = cameras.get(id=camera_id)

            ctx = {
                'cities': cities,
                'cameras': cameras,
                'chosen_city': chosen_city,
                'chosen_camera': camera,
            }

        return render(request, 'cameras.html', context=ctx)


@csrf_exempt
def detections(request):
    if request.method == 'GET':
        detections = Detection.objects.filter(verified=False)
        persons = detections.values(name=F('person__name'), photo=F('person__images__image_file')).distinct()
        ctx = { 'detections': detections, 'persons': persons }

        return render(request, 'detections.html', context=ctx)
    elif request.method == 'POST':
        person_name = request.POST['name']
        person = Person.objects.get(name=person_name)
        camera_name = request.POST['camera_name']
        camera = Camera.objects.get(name=camera_name)
        city_name = request.POST['city']
        city = City.objects.get(name=city_name)
        image_file = request.FILES['image']
        image = Image(image_file=image_file)

        set_save_location(f'{DETECTIONS_FOLDER_NAME}')
        image.save()

        detection = Detection(city=city, camera=camera, person=person, image=image)
        detection.save()

        return JsonResponse({ 'success': True })
    elif request.method == 'DELETE':
        data = JSONParser().parse(request)
        detection_id = data['id']

        detection = Detection.objects.get(id=detection_id)
        image = detection.image
        detection.delete()
        delete_file(image.image_file.path)
        image.delete()

        return JsonResponse({ 'success': True })


def verified(request):
    if request.method == 'GET':
        detections = Detection.objects.filter(verified=True)
        persons = detections.values(name=F('person__name')).distinct()
        ctx = { 'detections': detections, 'persons': persons }

        return render(request, 'verified.html', context=ctx)
    elif request.method == 'POST':
        id = JSONParser().parse(request)['id']
        detection = Detection.objects.get(id=id)
        detection.verified = True
        detection.save()

        return JsonResponse({ 'success': True })



def recognition(request):
    return render(request, 'recognition.html')


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
