from django.conf.urls import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'project.views.index'),
    url(r'^feedback$', direct_to_template, {'template':'feedback.html'}, name='feedback'),
)
