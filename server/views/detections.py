from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from rest_framework.parsers import JSONParser
from ..models import Detection, Person
from ..utils.storage import delete_file


def _get_detections(request, verified, render_page, person_id):
    detections = Detection.objects.filter(verified=verified).order_by('person__name')
    names = detections.values_list('person__name', flat=True).distinct()
    persons = Person.objects.filter(name__in=names)

    ctx = { 'elements': detections, 'persons': persons }

    if person_id:
        detections = detections.filter(person_id=person_id)
        ctx['elements'] = detections
        ctx['chosen'] = person_id

    paginator = Paginator(detections, 4)
    page = request.GET.get('page')

    if not page:
        page = 1

    ctx['elements'] = paginator.get_page(page)

    if len(detections) == 0:
        ctx['success'] = True
        ctx['message'] = 'There are no detections here!'

    return render(request, render_page, context=ctx)


def _delete_detection(request):
    data = JSONParser().parse(request)
    detection_id = data.get('id')

    if not detection_id:
        return JsonResponse({ 'error': True, 'message': 'Missing detection id!' })

    try:
        detection = Detection.objects.get(id=detection_id)
    except Detection.DoesNotExist:
        return JsonResponse({ 'error': True, 'message': 'Detection with this id does not exist!' })
    
    image = detection.image
    delete_file(image.image_file.path)
    # detection will be deleted recursively by the image
    image.delete()

    return JsonResponse({ 'success': True, 'message': 'Deleted the image!' })


@login_required
def detections(request, person_id=None):
    if request.method == 'GET':
        return _get_detections(request, False, 'detections.html', person_id)
    elif request.method == 'DELETE':
        return _delete_detection(request)


@login_required
def verified(request, person_id=None):
    if request.method == 'GET':
        return _get_detections(request, True, 'verified.html', person_id)
    elif request.method == 'POST':
        id = JSONParser().parse(request).get('id')
        
        if not id:
            return JsonResponse({ 'error': True, 'message': 'Missing id!' })

        try:
            detection = Detection.objects.get(id=id)
        except Detection.DoesNotExist:
            return JsonResponse({ 'error': True, 'message': 'Detection with this id does not exist!' })
            
        detection.verified = True
        detection.save()

        return JsonResponse({ 'success': True, 'message': 'Verified successfully!' })
    elif request.method == 'DELETE':
        return _delete_detection(request)