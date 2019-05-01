from django.shortcuts import render


def cameras(request):
    return render(request, 'cameras.html')


def persons(request):
    return render(request, 'persons.html')


def detections(request):
    return render(request, 'detections.html')


def verified(request):
    return render(request, 'verified.html')


def recognition(request):
    return render(request, 'recognition.html')