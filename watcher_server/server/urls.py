from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('cameras', views.cameras, name='cameras'),
    path('persons', views.persons, name='persons'),
    path('detections', views.detections, name='detections'),
    path('verified', views.verified, name="verified"),
    path('recognition', views.recognition, name="recognition")
]