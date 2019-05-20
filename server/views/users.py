from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .main import index
from ..forms import UsernameForm, PasswordForm


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and not request.user.is_authenticated:
            django_login(request, user)

            return redirect(index)
        else:
            context = { 'error': True, 'message': 'Login failed!' }

            return render(request, 'login.html', context)

    return render(request, 'login.html')


@login_required
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
            context = { 'error': True, 'message': 'Registration failed!' }
            return render(request, 'register.html', context)

    return render(request, 'register.html')


@login_required
def user_settings(request):
    ctx = {}

    if request.method == 'POST':
        username_form = UsernameForm(request.POST)
        password_form = PasswordForm(request.POST)
        updated_username = False
        updated_password = False
        initial_username = request.user.username
        current_user = get_object_or_404(User, username=initial_username)

        if username_form.is_valid():
            username_data = username_form.cleaned_data
            current_user.update(username=username_data['username'])
            request.user.username = username_data['username']
            updated_username = True

        if password_form.is_valid():
            password_data = password_form.cleaned_data
            current_user.set_password(password_data['password'])
            current_user.save()
            updated_password = True
        
        if updated_password and updated_username:
            ctx['success'] = True
            ctx['message'] = 'Updated username and password!'
        elif updated_password:
            ctx['success'] = True
            ctx['message'] = 'Updated password!'
        elif updated_username:
            ctx['success'] = True
            ctx['message'] = 'Updated username!'
        else:
            ctx['error'] = True
            ctx['message'] = 'Nothing updated!'

    return render(request, 'user-settings.html', context=ctx)