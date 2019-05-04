from django.shortcuts import render
from django.core.exceptions import ValidationError
from ..forms import AddPersonForm
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
        else:
            ctx = {'error': True, 'message': 'The form is invalid!'}
            return render(request, 'add-person.html', context=ctx)

    return render(request, 'add-person.html')


def persons(request):
    return render(request, 'persons.html')