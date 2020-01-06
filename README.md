# Watcher

Watcher is a web application that allows law enforcement to use a network of 
cameras to detect wanted people by utilizing face recognition.

## Available functionality:
1. registration, login, logout
2. user authorization
3. camera list and monitoring
4. adding and deleting wanted persons
5. notification on detection
6. system settings
7. system status - number of cameras, number of persons, number of found persons, etc.
8. camera software
9. list of unverified detections
10. list of verified detections
11. password and username changing
12. recognition from image taken from camera or file

## Python dependencies
face_recognition, opencv-python, flask, requests, pillow, scikit-learn, scipy, 
django, django-rest-framework, watchdog, channels

## How to run
To start the web server you can for example run python3 manage.py runserver 0.0.0.0:8000 
or deploy the server on a hosting service.
To start the camera software you can run python3 start_camera.py with arguments:
    1. central server url
    2. camera name
    3. city name
    4. camera ip
    5. camera port