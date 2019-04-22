from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse


def index(request):
    return render(request, 'base.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, email=None, password=password)
        user.save()

        print(User.objects.get(username='d'))

    return render(request, 'register.html')