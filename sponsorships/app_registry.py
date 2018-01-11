from tendenci.apps.registry.sites import site
from tendenci.apps.registry.base import AppRegistry, lazy_reverse
from sponsorships.models import Sponsorship


class SponsorshipRegistry(AppRegistry):
    version = '1.0'
    author = 'Jaime Lossada'
    author_email = 'jlosada87@hotmail.com'
    description = 'Allow sponsorships from anyone'

    url = {
        'add': lazy_reverse('sponsorship.add'),
        'search': lazy_reverse('sponsorship.search'),
    }


site.register(Sponsorship, SponsorshipRegistry)
