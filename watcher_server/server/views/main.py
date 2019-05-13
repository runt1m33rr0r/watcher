from django.shortcuts import render
from ..forms import SettingsForm
from ..models import Settings, SettingsCreationDate


def index(request):
    return render(request, 'home.html')


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


def user_settings(request):
    return render(request, 'user-settings.html')