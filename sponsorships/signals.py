def init_signals():
    from django.db.models.signals import post_save
    from sponsorships.models import Sponsorship
    from tendenci.apps.contributions.signals import save_contribution

    post_save.connect(save_contribution, sender=Sponsorship, weak=False)