subscribers = []


def subscribe(handler):
    subscribers.append(handler)


def detected(person_name, camera_name, city_name, detection_url):
    for sub in subscribers:
        sub(person_name, camera_name, city_name, detection_url)