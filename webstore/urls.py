from django.conf.urls import patterns, url, include
from webstore import views
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
    url(r'^category/(?P<id>.*)/$', views.webstore, name='webstore'),
    url(r'^search/autocomplete/$', views.autocomplete, name='autocomplete'),
    url(r'^searchStore/$',views.searchStore, name='searchStore'),
    url(r'^query/$', include('haystack.urls')),
    url(r'^addToCart/(?P<itemKey>[\w]+)/(?P<quantity>[\w]+)$',views.addToCart,name='addToCart'),
    url(r'^removeFromCart/(?P<itemKey>[\d]+)$',views.removeFromCart,name='removeFromCart'),
    url(r'^deleteCart/$', views.deleteCart, name='deleteCart'),
    url(r'^buttonTest/$', views.buttonTest, name='buttonTest'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^payment/$', views.payment, name='payment'),
)
