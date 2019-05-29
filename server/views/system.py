import base64
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..ai.classifier import process_frame
from ..models import Settings, SettingsCreationDate
from ..forms import SettingsForm, UploadImageForm


@login_required
def recognition(request):
    if request.method == 'GET':
        return render(request, 'recognition.html', context={ 'processed': '' })
    elif request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            image = data['image']
            processed = process_frame(image)
            processed = base64.b64encode(processed).decode('utf-8')

            return render(request, 'recognition.html', context={ 'processed': str(processed) })
        else:
            return render(request, 'recognition.html', context={ 'error': True, 'message': 'Invalid form!' })


@login_required
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