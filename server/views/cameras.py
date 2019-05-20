from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import City, Detection
from ..utils.storage import delete_file


@login_required
def cameras(request):
    if request.method == 'GET':
        cities = City.objects.all()

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
            chosen_city = cities.first()
            cameras = chosen_city.cameras.all()
            chosen_camera = cameras.first()
            ctx = {  
                'cities': cities, 
                'cameras': cameras,
                'chosen_city': chosen_city,
                'chosen_camera': chosen_camera,
            }

            if cameras.count() == 0:
                ctx['success'] = True
                ctx['message'] = 'There are no cameras in this city!'

        return render(request, 'cameras.html', context=ctx)


@login_required
def city(request, city_id):
    if request.method == 'GET':
        cities = City.objects.all()
        city = get_object_or_404(cities, id=city_id)
        cameras = city.cameras.all()
        chosen_camera = cameras.first()

        ctx = {
            'cities': cities, 
            'cameras': cameras,
            'chosen_city': city,
            'chosen_camera': chosen_camera,
        }

        if cameras.count() == 0:
            ctx['success'] = True
            ctx['message'] = 'There are no cameras in this city!'

        return render(request, 'cameras.html', context=ctx)
    elif request.method == 'DELETE':
        try:
            city = City.objects.get(id=city_id)
        except City.DoesNotExist:
            return JsonResponse({ 'error': True, 'message': 'City with this id does not exist!' })

        detections = Detection.objects.filter(city=city)
        for detection in detections:
            image = detection.image
            delete_file(image.image_file.path)
            # detection will be deleted recursively by the image
            image.delete()

        city.cameras.all().delete()
        city.delete()

        return JsonResponse({ 'success': True, 'message': 'Deleted city!' })


@login_required
def camera(request, city_id, camera_id):
    if request.method == 'GET':
        cities = City.objects.all()
        chosen_city = get_object_or_404(cities, id=city_id)
        cameras = chosen_city.cameras.all()
        camera = get_object_or_404(cameras, id=camera_id)

        ctx = {
            'cities': cities,
            'cameras': cameras,
            'chosen_city': chosen_city,
            'chosen_camera': camera,
        }

        return render(request, 'cameras.html', context=ctx)