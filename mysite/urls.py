from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^blogadmin/', include(admin.site.urls)),
    url(r'^', include('frontend.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^webstore/', include('webstore.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^companion/', include('companion.urls')),
    url(r'^user/', include('user_management.urls')),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
