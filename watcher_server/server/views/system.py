import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.static import serve
from ..ai.classifier import classifier_path
from ..models import ClassifierCreationDate


def cameras(request):
    return render(request, 'cameras.html')


def detections(request):
    return render(request, 'detections.html')


def verified(request):
    return render(request, 'verified.html')


def recognition(request):
    return render(request, 'recognition.html')


def get_classifier_file(request):
    if request.method == 'GET':
        return serve(request, os.path.basename(classifier_path), os.path.dirname(classifier_path))


def get_classifier_date(request):
    if request.method == 'GET':
        if ClassifierCreationDate.objects.filter().exists():
            date = ClassifierCreationDate.objects.get()

            return JsonResponse({ 'date': date.date })
        
        return JsonResponse({ 'date': None })