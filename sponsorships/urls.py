from django.conf.urls import patterns, url

urlpatterns = patterns('sponsorships.views',
    url(r'^sponsorships/$', 'add', name="sponsorships.add"),
    url(r'^sponsorships/conf/(?P<id>\d+)/$', 'add_confirm', name="sponsorships.add_confirm"),
    url(r'^sponsorships/(?P<id>\d+)/$', 'detail', name="sponsorships.view"),
    url(r'^sponsorships/receipt/(?P<id>\d+)/(?P<guid>[\d\w-]+)/$', 'receipt', name="sponsorships.receipt"),
    url(r'^sponsorships/search/$', 'search', name="sponsorships.search"),
)