from django.shortcuts import render


def cameras(request):
    return render(request, 'cameras.html')


def persons(request):
    return render(request, 'persons.html')