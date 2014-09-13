from django.contrib import admin
from .models import Person, IncomingRequest

admin.site.register(Person)
admin.site.register(IncomingRequest)

