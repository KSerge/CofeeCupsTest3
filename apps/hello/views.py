from django.shortcuts import render
from .models import Person
from django.template import RequestContext


def index(request):
    try:
        person = Person.objects.get(pk=1)
    except Person.DoesNotExist:
        person = Person()
    request_context = RequestContext(request,  {'person': person})
    return render(request, 'hello/index.html', request_context)
