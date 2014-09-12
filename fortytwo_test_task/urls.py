from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/', include('apps.hello.urls')),
    url(r'^$', RedirectView.as_view(pattern_name='index'), name='default'),
)
