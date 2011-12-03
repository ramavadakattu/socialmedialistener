from django.conf.urls.defaults import *



urlpatterns = patterns('paypallistener.views',
                url(r'^$','showPopularStories',name="popularurl"),
                url(r'page(?P<pageno>\d+)/$','showPopularStories',name="popularurl2"),
                url(r'tag/(?P<tagid>[0-9]+)/$','getStoriesByTag',name="tagstoriesurl"),
                 url(r'totalshares/$','getTotalShares',name="totalsharesurl"),
    )



