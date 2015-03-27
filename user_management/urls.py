from django.conf.urls import patterns, url
from user_management import views

urlpatterns = patterns('',
    url('^$', views.index),
    url('^profile/?', views.profile),
    url('^register/?', views.register_index),
    url('^login/?$', views.login_index),
    url('^logout/?$', views.logout_user),
    url('^change-password/?$', views.changepw_index),
    url('^change-email/?$', views.change_email_index),
    url('^order-history/?$', views.order_history),
    url('^activate/(?P<confirmation_code>\w+)/(?P<username>\w+)/?$', views.activate),
)
