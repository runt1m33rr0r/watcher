import os
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from ..forms import AddPersonForm, UploadImageForm
from ..models import Person, Image
from ..utils.storage import set_save_location, delete_file


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
            except ValidationError as e:
                ctx = {'error': True, 'message': e}
                return render(request, 'add-person.html', context=ctx)
            
            person.save()
            set_save_location(person.name)
            image.save()
            person.images.add(image)

            ctx = {'success': True, 'message': 'Created person!'}
            return render(request, 'add-person.html', context=ctx)
        else:
            ctx = {'error': True, 'message': 'The data provided is invalid!'}
            return render(request, 'add-person.html', context=ctx)

    return render(request, 'add-person.html')


def persons(request, person_id=None):
    if request.method == 'GET':
        persons = Person.objects.all()
        ctx = {}

        if persons.count() == 0:
            ctx = {  
                'persons': [], 
                'images': [],
                'chosen': None,
                'success': True, 
                'message': 'There are no wanted persons in the system!' 
            }
        else:
            if person_id:
                chosen = Person.objects.get(id=person_id)
                ctx = {
                    'persons': persons,
                    'chosen': chosen,
                    'images': chosen.images.all()
                }
            else:
                return redirect(f'/persons/{persons.first().id}')

        return render(request, 'persons.html', ctx)


def person_images(request, person_id):
    if request.method == 'POST':
        persons = Person.objects.all()
        chosen = Person.objects.get(id=person_id)
        images = chosen.images.all()
        ctx = {
            'persons': persons,
            'chosen': chosen,
            'images': images
        }
        form = UploadImageForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            person = Person.objects.get(id=person_id)
            image = Image(image_file=data['image'])

            try:
                image.full_clean()
            except ValidationError as e:
                ctx['error'] = True
                ctx['message'] = e
                return render(request, 'persons.html', context=ctx)

            set_save_location(person.name)
            image.save()
            person.images.add(image)
            
            ctx['success'] = True
            ctx['message'] = 'Added image!'
        else:
            ctx['error'] = True
            ctx['message'] = 'The data provided is invalid!'
        
        return render(request, 'persons.html', context=ctx)


def person_image(request, person_id, image_id):
    if request.method == 'DELETE':
        person = Person.objects.get(id=person_id)
        image = person.images.get(id=image_id)
        
        delete_file(image.image_file.path)
        image.delete()

        return JsonResponse({ 'success': True, 'message': 'Image deleted!' })
