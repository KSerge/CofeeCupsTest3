from django.contrib import admin
from .models import Person, IncomingRequest


class IncomingRequestAdmin(admin.ModelAdmin):
    fields = ('path', 'priority', 'visiting_date',)
    readonly_fields = ('visiting_date',)

admin.site.register(Person)
admin.site.register(IncomingRequest, IncomingRequestAdmin)

