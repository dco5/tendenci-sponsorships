# settings: label, sponsorshipspaymenttypes, sponsorshipsallocations, 
#           sponsorshipsrecipients, 
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from tendenci.apps.invoices.models import Invoice
from tendenci.apps.site_settings.utils import get_setting


def sponsorship_inv_add(user, sponsorship, **kwargs):
    inv = Invoice()
    inv.title = "Sponsorship Invoice"
    inv.bill_to = sponsorship.first_name + ' ' + sponsorship.last_name
    inv.bill_to_first_name = sponsorship.first_name
    inv.bill_to_last_name = sponsorship.last_name
    inv.bill_to_company = sponsorship.company
    inv.bill_to_address = sponsorship.address
    inv.bill_to_city = sponsorship.city
    inv.bill_to_state = sponsorship.state
    inv.bill_to_zip_code = sponsorship.zip_code
    inv.bill_to_country = "US"
    inv.bill_to_phone = sponsorship.phone
    inv.bill_to_email = sponsorship.email
    inv.ship_to = sponsorship.first_name + ' ' + sponsorship.last_name
    inv.ship_to_first_name = sponsorship.first_name
    inv.ship_to_last_name = sponsorship.last_name
    inv.ship_to_company = sponsorship.company
    inv.ship_to_address = sponsorship.address
    inv.ship_to_city = sponsorship.city
    inv.ship_to_state = sponsorship.state
    inv.ship_to_zip_code = sponsorship.zip_code
    inv.ship_to_country = "US"
    inv.ship_to_phone = sponsorship.phone
    # self.ship_to_fax = make_payment.fax
    inv.ship_to_email = sponsorship.email
    inv.terms = "Due on Receipt"
    inv.due_date = datetime.now()
    inv.ship_date = datetime.now()
    inv.message = 'Thank You.'
    inv.status = True

    inv.estimate = True
    inv.status_detail = 'tendered'
    inv.object_type = ContentType.objects.get(app_label=sponsorship._meta.app_label,
                                              model=sponsorship._meta.model_name)
    inv.object_id = sponsorship.id
    inv.subtotal = sponsorship.sponsorship_amount
    inv.total = sponsorship.sponsorship_amount
    inv.balance = sponsorship.sponsorship_amount

    inv.save(user)
    sponsorship.invoice = inv

    return inv


def sponsorship_email_user(request, sponsorship, invoice, **kwargs):
    from django.core.mail.message import EmailMessage
    from django.template.loader import render_to_string
    from django.conf import settings
    from django.template import RequestContext

    subject = render_to_string('sponsorships/email_user_subject.txt',
                               {'sponsorships': sponsorship},
                               context_instance=RequestContext(request))
    body = render_to_string('sponsorships/email_user.txt',
                            {'sponsorships': sponsorship, 'invoice': invoice},
                            context_instance=RequestContext(request))

    sender = settings.DEFAULT_FROM_EMAIL
    recipient = sponsorship.email
    msg = EmailMessage(subject, body, sender, [recipient])
    msg.content_subtype = 'html'
    try:
        msg.send()
    except:
        pass


def get_payment_method_choices(user):
    if user.profile.is_superuser:
        return (('paid - check', 'User paid by check'),
                ('paid - cc', 'User paid by credit card'),
                ('Credit Card', 'Make online payment NOW'),)
    else:
        sponsorship_payment_types = get_setting('module', 'sponsorships', 'sponsorshippaymenttypes')
        if sponsorship_payment_types:
            sponsorship_payment_types_list = sponsorship_payment_types.split(',')
            sponsorship_payment_types_list = [item.strip() for item in sponsorship_payment_types_list]

            return [(item, item) for item in sponsorship_payment_types_list]
        else:
            return ()


def get_allocation_choices(user, allocation_str):
    # allocation_str = get_setting('module', 'sponsorships', 'sponsorshipsallocations')
    if allocation_str:
        allocation_list = allocation_str.split(',')
        allocation_list = [item.strip() for item in allocation_list]

        return [(item, item) for item in allocation_list]
    else:
        return ()


def get_preset_amount_choices(preset_amount_str):
    if preset_amount_str:
        preset_amount_list = preset_amount_str.split(',')
        preset_amount_list = [item.strip() for item in preset_amount_list]

        return [(item, item) for item in preset_amount_list]
    else:
        return ()
