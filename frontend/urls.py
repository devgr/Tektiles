from django.conf.urls import patterns, url
from django.contrib import admin 
from frontend import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^contact/$', views.contact, name='contact'),
        url(r'^$', 'index', name='index'),
 )
