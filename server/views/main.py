from django.shortcuts import render
from django.contrib.auth.models import User
from ..models import Detection, Person, Camera, City


def index(request):
    ctx = {
        'verified_count': Detection.objects.filter(verified=True).count(),
        'unverified_count': Detection.objects.filter(verified=False).count(),
        'wanted_count': Person.objects.all().count(),
        'cameras_count': Camera.objects.all().count(),
        'cities_count': City.objects.all().count(),
        'users_count': User.objects.all().count(),
    }

    return render(request, 'home.html', context=ctx)