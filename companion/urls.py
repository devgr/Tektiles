from django.conf.urls import patterns, url
from companion import views


urlpatterns = patterns('',
    url(r'^category/(?P<id>.*)/$', views.companion, name='companion'),
    url(r'^app/(?P<id>.*)/$', views.app, name='app'),
    url(r'^topic/(?P<id>.*)/$', views.topic, name='topic'), 
    url(r'^fabric/(?P<id>.*)/$', views.fabric, name='fabric'),  

)
