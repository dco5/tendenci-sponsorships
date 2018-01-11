from django.contrib import admin
from sponsorships.models import Sponsorship
from tendenci.apps.donations.forms import DonationAdminForm


class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'sponsorship_amount', 'payment_method']
    form = DonationAdminForm


admin.site.register(Sponsorship, SponsorshipAdmin)
