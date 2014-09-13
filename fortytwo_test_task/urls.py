from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/', include('apps.hello.urls')),
    url(r'^$', RedirectView.as_view(pattern_name='index'), name='default'),
)