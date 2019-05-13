from django.shortcuts import render
from django.contrib.auth.models import User
from ..forms import SettingsForm
from ..models import Settings, SettingsCreationDate, Detection, Person, Camera, City


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


def settings(request):  
    if request.method == 'GET':
        settings_data = Settings.objects.get_or_create()

        return render(request, 'settings.html', context={ 'settings': settings_data[0] })
    elif request.method == 'POST':
        ctx = {}
        form = SettingsForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            settings_data = Settings.objects.update_or_create(defaults=data)
            SettingsCreationDate.objects.update_or_create()
            ctx['settings'] = settings_data[0]
        else:
            ctx['error'] = True
            ctx['message'] = 'Ivalid input!'

        return render(request, 'settings.html', context=ctx)