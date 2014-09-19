from django.contrib import admin
from .models import Person, IncomingRequest, ModelObjectsTracker


class IncomingRequestAdmin(admin.ModelAdmin):
    fields = ('path', 'priority', 'visiting_date',)
    readonly_fields = ('visiting_date',)
    list_display = ['path', 'visiting_date', 'priority', ]


class ModelObjectsTrackerAdmin(admin.ModelAdmin):
    fields = ('model_name', 'type_of_event', 'created_date',)
    readonly_fields = ('created_date',)
    list_display = ['model_name', 'type_of_event', 'created_date', ]

admin.site.register(Person)
admin.site.register(IncomingRequest, IncomingRequestAdmin)
admin.site.register(ModelObjectsTracker, ModelObjectsTrackerAdmin)

