from django.shortcuts import render
from .models import Person, IncomingRequest
from django.template import RequestContext
from django.conf import settings


def context_processor(request):
    return {
        'settings': settings,
    }


def index(request):
    try:
        person = Person.objects.get(pk=1)
    except Person.DoesNotExist:
        person = Person()
    request_context = RequestContext(request,  {'person': person})
    return render(request, 'hello/index.html', request_context)


def view_requests(request):
    stored_requests = IncomingRequest.objects.order_by('visiting_date')[0:10]
    request_context = RequestContext(
        request,
        {'requests': stored_requests})
    return render(request, 'hello/requests.html', request_context)


def edit(request):
    pass


def login(request):
    pass


def logout(request):
    pass