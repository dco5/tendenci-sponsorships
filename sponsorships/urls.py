from django.conf.urls import patterns, url

urlpatterns = patterns(
    'sponsorships.views',
    url(r'^sponsorships/$', 'add', name="sponsorship.add"),

    url(r'^sponsorships/event/(?P<id>\d+)/$', 'add', name="sponsorship.add_with_event"),

    url(r'^sponsorships/conf/(?P<id>\d+)/$', 'add_confirm', name="sponsorship.add_confirm"),
    url(r'^sponsorships/(?P<id>\d+)/$', 'detail', name="sponsorship.view"),
    url(r'^sponsorships/receipt/(?P<id>\d+)/(?P<guid>[\d\w-]+)/$', 'receipt',
        name="sponsorship.receipt"),
    url(r'^sponsorships/search/$', 'search', name="sponsorship.search"),

    url(r'^event/sponsorship-level/(?P<event_id>\d+)/$', 'edit_sponsorship_level', name='sponsorship.level.edit'),
    url(r'^event/sponsors/(?P<event_id>\d+)/$', 'event_sponsors', name="event_sponsors"),
)
