from django.shortcuts import render
from .models import Person, IncomingRequest
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .forms import PersonForm, UserForm, UserLoginForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

SAVE_FORM_ERRORS_MESSAGE = 'Provided data is not correct. Please review all errors.'
INVALID_LOGIN_MESSAGE = 'Invalid login data'


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
            if request.is_ajax():
                data = {'redirect_url': reverse('index')}
                return HttpResponse(json.dumps(data), content_type="application/json")
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


def login_user(request):
    message = ''
    if request.method == 'POST':
        user_form = UserLoginForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                message = "Your account is disabled"
        else:
            message = INVALID_LOGIN_MESSAGE
    else:
        user_form = UserLoginForm()

    request_context = RequestContext(
        request,
        {
            'form': user_form,
            'message': message
        })

    return render(request, 'hello/login.html', request_context)


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
