from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('cameras', views.cameras, name='cameras'),
    path('cameras/<int:city_id>/', views.city, name='city'),
    path('cameras/<int:city_id>/<int:camera_id>', views.camera, name='camera'),
    path('cameras/register', views.register_camera, name='register_camera'),

    path('persons', views.persons, name='persons'),
    path('persons/add', views.add_person, name='add_person'),
    path('persons/<int:person_id>/', views.persons, name='person'),
    path('persons/<int:person_id>/images/', views.person_images, name='person_images'),
    path('persons/<int:person_id>/images/<int:image_id>', views.person_image, name='person_image'),
    
    path('detections', views.detections, name='detections'),
    path('detections/<int:person_id>', views.detections, name='detections_by_id'),
    path('verified', views.verified, name='verified'),
    path('verified/<int:person_id>', views.verified, name='verified_by_id'),
    
    path('recognition', views.recognition, name='recognition'),
    path('settings', views.settings, name='settings'),

    path('user', views.user_settings, name='user_settings'),
    path('user/login', views.login, name='login'),
    path('user/register', views.register, name='register'),
    path('user/logout', views.logout, name='logout'),

    path('classifier', views.get_classifier_file, name='get_classifier'),
    path('classifier/date', views.get_classifier_date, name='get_classifier_date'),

    path('rest/settings/date', views.get_settings_date, name='get_settings_date'),
    path('rest/settings', views.get_settings, name='get_settings'),
]