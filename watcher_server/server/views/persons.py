from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from ..forms import AddPersonForm, UploadImageForm
from ..models import Person, Image


def add_person(request):
    if request.method == 'POST':
        form = AddPersonForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            image = Image(image_file=data['image'])
            person = Person(name=data['name'])

            try:
                image.full_clean()
                person.full_clean()
            except ValidationError as e:
                ctx = {'error': True, 'message': e}
                return render(request, 'add-person.html', context=ctx)
            
            person.save()
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
    elif request.method == 'POST':
        ctx = {}
        persons = Person.objects.all()
        chosen = Person.objects.get(id=person_id)
        images = chosen.images.all()
        form = UploadImageForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            image = Image(image_file=data['image'])
            person = Person.objects.get(id=person_id)

            try:
                image.full_clean()
            except ValidationError as e:
                ctx = {
                    'persons': persons,
                    'chosen': chosen,
                    'images': images,
                    'error': True, 'message': e
                }
                return render(request, 'persons.html', context=ctx)

            image.save()
            person.images.add(image)
            
            ctx = {
                'persons': persons,
                'chosen': chosen,
                'images': images,
                'success': True, 
                'message': 'Added image!'
            }
        else:
            ctx = {
                'persons': persons,
                'chosen': chosen,
                'images': images,
                'error': True, 
                'message': 'The data provided is invalid!'
            }
        
        return render(request, 'persons.html', context=ctx)
