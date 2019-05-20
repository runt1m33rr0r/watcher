from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..forms import AddPersonForm, UploadImageForm
from ..models import Person, Image, Detection
from ..utils.storage import set_save_location, delete_file, PERSONS_FOLDER_NAME


@login_required
def add_person(request):
    if request.method == 'POST':
        form = AddPersonForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            person = Person(name=data['name'])
            image = Image(image_file=data['image'])

            try:
                image.full_clean()
                person.full_clean()
            except ValidationError:
                ctx = { 'error': True, 'message': 'Invalid input data!' }

                return render(request, 'add-person.html', context=ctx)
            
            person.save()
            set_save_location(f'{PERSONS_FOLDER_NAME}/{person.name}')
            image.save()
            person.images.add(image)
            ctx = { 'success': True, 'message': 'Created person!' }

            return render(request, 'add-person.html', context=ctx)
        else:
            ctx = { 'error': True, 'message': 'The data provided is invalid!' }

            return render(request, 'add-person.html', context=ctx)

    return render(request, 'add-person.html')


@login_required
def persons(request, person_id=None):
    if request.method == 'GET':
        persons_data = Person.objects.all()
        ctx = {}

        if persons_data.count() == 0:
            ctx = {  
                'persons': [], 
                'images': [],
                'chosen': None,
                'success': True, 
                'message': 'There are no wanted persons in the system!' 
            }
        else:
            if person_id:
                chosen = get_object_or_404(Person, id=person_id)
                ctx = {
                    'persons': persons_data,
                    'chosen': chosen,
                    'images': chosen.images.all()
                }
            else:
                return redirect(persons, person_id=persons_data.first().id)

        return render(request, 'persons.html', ctx)
    elif request.method == 'DELETE':
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return JsonResponse({ 'error': True, 'message': 'Person does not exist!' })

        person_images = person.images.all()
        person_detections = Detection.objects.filter(person=person)

        for image in person_images:
            delete_file(image.image_file.path)
            image.delete()

        for detection in person_detections:
            delete_file(detection.image.image_file.path)
            detection.image.delete()

        person.delete()

        return JsonResponse({ 'success': True, 'message': 'Person deleted!' })


@login_required
def person_images(request, person_id):
    if request.method == 'POST':
        persons = Person.objects.all()
        chosen = get_object_or_404(Person, id=person_id)
        images = chosen.images.all()
        ctx = {
            'persons': persons,
            'chosen': chosen,
            'images': images
        }
        form = UploadImageForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            person = get_object_or_404(Person, id=person_id)
            image = Image(image_file=data['image'])

            try:
                image.full_clean()
            except ValidationError:
                ctx['error'] = True
                ctx['message'] = 'Invalid image!'
                return render(request, 'persons.html', context=ctx)

            set_save_location(f'{PERSONS_FOLDER_NAME}/{person.name}')
            image.save()
            person.images.add(image)
            
            ctx['success'] = True
            ctx['message'] = 'Added image!'
        else:
            ctx['error'] = True
            ctx['message'] = 'The data provided is invalid!'
        
        return render(request, 'persons.html', context=ctx)


@login_required
def person_image(request, person_id, image_id):
    if request.method == 'DELETE':
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return JsonResponse({ 'error': True, 'message': 'Person does not exist!' })

        try:
            image = person.images.get(id=image_id)
        except Image.DoesNotExist:
            return JsonResponse({ 'error': True, 'message': 'Image does not exist!' })
        
        delete_file(image.image_file.path)
        image.delete()

        return JsonResponse({ 'success': True, 'message': 'Image deleted!' })
