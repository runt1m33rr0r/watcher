import os
from django.shortcuts import render
from django.http import HttpResponse
from django.views.static import serve
from ..ai.classifier import classifier_path


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