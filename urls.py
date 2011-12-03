from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
            (r'^admin/(.*)', admin.site.root),
            (r'^ebaylistener/', include('paypallistener.urls')),      
     )



if settings.DEBUG:    
    urlpatterns += patterns('',
            url(r'^appmedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        )