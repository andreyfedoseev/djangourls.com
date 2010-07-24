from django.conf import settings
from django.conf.urls.defaults import patterns, handler500, handler404, url,\
    include
from django.contrib import admin
from django.views.generic.simple import direct_to_template


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/(.*)', admin.site.root),
    url(r'^$', 'project.views.index'),
    url(r'^feedback$', direct_to_template, {'template':'feedback.html'}, name='feedback'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'', include('staticfiles.urls')),
    )