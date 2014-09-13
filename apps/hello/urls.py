from django.conf.urls import url
from .views import index, view_requests

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^requests/$', view_requests, name='requests'),
]