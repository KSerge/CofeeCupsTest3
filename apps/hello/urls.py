from django.conf.urls import url
from .views import index, view_requests, edit, login, logout

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^requests/$', view_requests, name='requests'),
    url(r'login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^edit/$', edit, name='edit'),
]