from django.shortcuts import render
from .models import Person, IncomingRequest
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import PersonForm, UserForm
from django.core.urlresolvers import reverse

SAVE_FORM_ERRORS_MESSAGE = 'Provided data is not correct. Please review all errors.'


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
    try:
        person = Person.objects.get(pk=1)
        user = User.objects.get(pk=person.user_id)
    except Person.DoesNotExist, User.DoesNotExists:
        person = Person()
        user = User()
    message = ''
    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES, instance=person)
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid() and person_form.is_valid():
            user_form.save()
            person_form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            message = SAVE_FORM_ERRORS_MESSAGE
    else:
        person_form = PersonForm(instance=person)
        user_form = UserForm(instance=user)

    request_context = RequestContext(
        request,
        {
            'person': person,
            'person_form': person_form,
            'user_form': user_form,
            'message': message
        })
    return render(request, 'hello/edit.html', request_context)


def login(request):
    pass


def logout(request):
    pass