from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from project.views import *


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^ajax_search/$', ajax_user_details, name='ajax_search'),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
