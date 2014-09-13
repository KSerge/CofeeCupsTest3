from django.conf.urls import url
from .views import index, view_requests, edit, login_user, logout_user

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^requests/$', view_requests, name='requests'),
    url(r'login/$', login_user, name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^edit/$', edit, name='edit'),
]