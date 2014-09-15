from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

CREATE_ACTION_NAME = 'create'
EDIT_ACTION_NAME = 'edit'
DELETE_ACTION_NAME = 'delete'

class Person(models.Model):
    user = models.OneToOneField(User, null=True)
    date_of_birth = models.DateField(auto_now=False, null=True, blank=True)
    bio = models.CharField(max_length=254, null=True, blank=True)
    jabber = models.EmailField(max_length=100, null=True, blank=True)
    skype = models.CharField(max_length=50, null=True, blank=True)
    other_contacts = models.CharField(max_length=254, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile", null=True, blank=True)


class IncomingRequest(models.Model):
    path = models.CharField(max_length=500)
    visiting_date = models.DateTimeField(auto_now=True)
    priority = models.PositiveSmallIntegerField(default=0)


class ModelObjectsTracker(models.Model):
    model_name = models.CharField(max_length=50, null=False, blank=False)
    type_of_event = models.CharField(max_length=10, null=False, blank=False)
    created_date = models.DateTimeField(default=timezone.now())
