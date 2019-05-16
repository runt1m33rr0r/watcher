from django.shortcuts import render
from ..models import City


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


def city(request, city_id):
    if request.method == 'GET':
        cities = City.objects.all()
        city = cities.get(id=city_id)
        cameras = city.cameras.all()
        chosen_camera = city.cameras.first()

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


def camera(request, city_id, camera_id):
    if request.method == 'GET':
        cities = City.objects.all()
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