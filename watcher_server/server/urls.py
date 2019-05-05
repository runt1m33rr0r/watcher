from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),

    path('cameras', views.cameras, name='cameras'),
    path('cameras/register', views.register_camera, name='register_camera'),

    path('persons', views.persons, name='persons'),
    path('persons/add', views.add_person, name='add_person'),
    path('persons/<int:person_id>/', views.persons, name='person'),
    path('persons/<int:person_id>/images/', views.person_images, name='person_images'),
    path('persons/<int:person_id>/images/<int:image_id>', views.person_image, name='person_image'),
    
    path('detections', views.detections, name='detections'),
    path('verified', views.verified, name="verified"),
    path('recognition', views.recognition, name="recognition")
]