from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login as django_login, logout as django_logout


def index(request):
    return render(request, 'cameras.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and not request.user.is_authenticated:
            django_login(request, user)

            return redirect(index)
        else:
            context = {'error': True, 'message': 'Login failed!'}

            return render(request, 'login.html', context)

    return render(request, 'login.html')


def logout(request):
    django_logout(request)

    return redirect(index)


def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.create_user(username=username, email=None, password=password)
            user.save()

            return redirect(login)
        except IntegrityError:
            context = {'error': True, 'message': 'Registration failed!'}
            return render(request, 'register.html', context)

    return render(request, 'register.html')