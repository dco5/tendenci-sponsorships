import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from tendenci.apps.invoices.models import Invoice
from sponsorships.managers import SponsorshipManager
from tendenci.apps.events.models import Event


class SponsorshipLevel(models.Model):
    event = models.ForeignKey(Event, related_name='sponsorship_levels')
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    limit = models.IntegerField(default=1)

    uses_fix_amount = models.BooleanField(default=False)

    fix_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    max_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        app_label = 'sponsorships'
        verbose_name = 'Sponsorship Level'
        verbose_name_plural = 'Sponsorship Levels'

    def __unicode__(self):
        return self.name


class Sponsorship(models.Model):
    guid = models.CharField(max_length=50)
    user = models.ForeignKey(User, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    company = models.CharField(max_length=50, default='', blank=True, null=True)
    address = models.CharField(max_length=100, default='', blank=True, null=True)
    address2 = models.CharField(_('address line 2'), max_length=100, default='', blank=True, null=True)
    city = models.CharField(max_length=50, default='', blank=True, null=True)
    state = models.CharField(max_length=50, default='', blank=True, null=True)
    zip_code = models.CharField(max_length=50, default='', blank=True, null=True)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)

    referral_source = models.CharField(_('referred by'), max_length=200, default='', blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    sponsorship_amount = models.DecimalField(max_digits=10, decimal_places=2)

    allocation = models.CharField(max_length=150, default='', blank=True, null=True)

    payment_method = models.CharField(max_length=50, default='cc')
    invoice = models.ForeignKey(Invoice, blank=True, null=True)

    create_dt = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, null=True, related_name="sponsorship_creator")
    creator_username = models.CharField(max_length=50, null=True)
    owner = models.ForeignKey(User, null=True, related_name="sponsorship_owner")
    owner_username = models.CharField(max_length=50, null=True)

    status_detail = models.CharField(max_length=50, default='estimate')
    status = models.NullBooleanField(default=True)

    level = models.ForeignKey(SponsorshipLevel, blank=True, null=True, related_name='sponsorships')

    event = models.ForeignKey(Event, blank=True, null=True, related_name="sponsorships")

    objects = SponsorshipManager()

    class Meta:
        app_label = 'sponsorships'

    def save(self, user=None, *args, **kwargs):
        if not self.id:
            self.guid = str(uuid.uuid1())
            if user and user.id:
                self.creator = user
                self.creator_username = user.username
        if user and user.id:
            self.owner = user
            self.owner_username = user.username

        super(Sponsorship, self).save(*args, **kwargs)

    # Called by payments_pop_by_invoice_user in Payment model.
    def get_payment_description(self, inv):
        """
        The description will be sent to payment gateway and displayed on invoice.
        If not supplied, the default description will be generated.
        """
        return 'Sponsorship Invoice Payment to be an event Sponsor. \nEvent: %s ' % (self.allocation,)

    def make_acct_entries(self, user, inv, amount, **kwargs):
        """
        Make the accounting entries for the sponsorships sale
        """
        from tendenci.apps.accountings.models import Acct, AcctEntry, AcctTran
        from tendenci.apps.accountings.utils import make_acct_entries_initial, make_acct_entries_closing

        ae = AcctEntry.objects.create_acct_entry(user, 'invoice', inv.id)
        if not inv.is_tendered:
            make_acct_entries_initial(user, ae, amount)
        else:
            # payment has now been received
            make_acct_entries_closing(user, ae, amount)

            # #CREDIT sponsorships SALES
            acct_number = self.get_acct_number()
            acct = Acct.objects.get(account_number=acct_number)
            AcctTran.objects.create_acct_tran(user, ae, acct, amount * (-1))

    def get_acct_number(self, discount=False):
        if discount:
            return 465100
        else:
            return 405100

    def auto_update_paid_object(self, request, payment):
        """
        Update the object after online payment is received.
        """
        # email to admin
        try:
            from tendenci.apps.notifications import models as notification
        except:
            notification = None
        from tendenci.apps.perms.utils import get_notice_recipients

        recipients = get_notice_recipients('module', 'sponsorships', 'sponsorshiprecipients')
        if recipients:
            if notification:
                extra_context = {
                    'sponsorships': self,
                    'invoice': payment.invoice,
                    'request': request,
                }
                notification.send_emails(recipients, 'sponsorships', extra_context)
