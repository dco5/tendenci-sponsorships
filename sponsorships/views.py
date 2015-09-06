from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from sponsorships.forms import SponsorshipForm
from sponsorships.utils import sponsorship_inv_add, sponsorship_email_user
from sponsorships.models import Sponsorship
from tendenci.apps.site_settings.utils import get_setting
from tendenci.apps.base.forms import CaptchaForm
from tendenci.apps.base.http import Http403
from tendenci.apps.base.utils import tcurrency
from tendenci.apps.event_logs.models import EventLog
from tendenci.apps.perms.utils import get_notice_recipients
from tendenci.apps.perms.utils import has_perm
from tendenci.apps.base.utils import get_unique_username
from tendenci.apps.profiles.models import Profile

try:
    from tendenci.apps.notifications import models as notification
except:
    notification = None


def add(request, form_class=SponsorshipForm, template_name="sponsorships/add.html"):
    use_captcha = get_setting('site', 'global', 'captcha')

    if request.method == "POST":
        form = form_class(request.POST, user=request.user)
        captcha_form = CaptchaForm(request.POST)
        if not use_captcha:
            del captcha_form.fields['captcha']

        if form.is_valid() and captcha_form.is_valid():
            sponsorship = form.save(commit=False)
            sponsorship.payment_method = sponsorship.payment_method.lower()
            # we might need to create a user record if not exist
            if request.user.is_authenticated():
                user = request.user
            else:
                try:
                    user = User.objects.get(email=sponsorship.email)
                except:
                    user = request.user

            if not user.is_anonymous():
                sponsorship.user = user
                sponsorship.creator = user
                sponsorship.creator_username = user.username
            else:
                # this is anonymous user donating and we didn't find their user record in the system,
                # so add a new user
                user = User()
                user.first_name = sponsorship.first_name
                user.last_name = sponsorship.last_name
                user.email = sponsorship.email
                user.username = get_unique_username(user)
                user.set_password(User.objects.make_random_password(length=8))
                user.is_active = 0
                user.save()

                profile_kwarg = {'user':user,
                                 'company':sponsorship.company,
                                 'address':sponsorship.address,
                                 'address2':sponsorship.address2,
                                 'city':sponsorship.city,
                                 'state':sponsorship.state,
                                 'zipcode':sponsorship.zip_code,
                                 'phone':sponsorship.phone}
                if request.user.is_anonymous():
                    profile_kwarg['creator'] = user
                    profile_kwarg['creator_username'] = user.username
                    profile_kwarg['owner'] = user
                    profile_kwarg['owner_username'] = user.username
                else:
                    profile_kwarg['creator'] = request.user
                    profile_kwarg['creator_username'] = request.user.username
                    profile_kwarg['owner'] = request.user
                    profile_kwarg['owner_username'] = request.user.username

                profile = Profile.objects.create(**profile_kwarg)
                profile.save()

            sponsorship.save(user)

            # create invoice
            invoice = sponsorship_inv_add(user, sponsorship)
            # updated the invoice_id for mp, so save again
            sponsorship.save(user)

            if request.user.profile.is_superuser:
                if sponsorship.payment_method in ['paid - check', 'paid - cc']:
                    # the admin accepted payment - mark the invoice paid
                    invoice.tender(request.user)
                    invoice.make_payment(request.user, sponsorship.sponsorship_amount)

            # send notification to administrators
            # get admin notice recipients
            if not sponsorship.payment_method.lower() in ['cc', 'credit card', 'paypal']:
                # email to admin (if payment type is credit card email is not sent until payment confirmed)
                recipients = get_notice_recipients('module', 'sponsorships', 'sponsorshipsrecipients')
                if recipients:
                    if notification:
                        extra_context = {
                            'sponsorship': sponsorship,
                            'invoice': invoice,
                            'request': request,
                        }
                        notification.send_emails(recipients,'sponsorship_added', extra_context)

            # email to user
            email_receipt = form.cleaned_data['email_receipt']
            if email_receipt:
                sponsorship_email_user(request, sponsorship, invoice)

            EventLog.objects.log(instance=sponsorship)

            # redirect to online payment or confirmation page
            if sponsorship.payment_method.lower() in ['cc', 'credit card', 'paypal']:
                return HttpResponseRedirect(reverse('payment.pay_online', args=[invoice.id, invoice.guid]))
            else:
                return HttpResponseRedirect(reverse('sponsorship.add_confirm', args=[sponsorship.id]))
    else:
        form = form_class(user=request.user)
        captcha_form = CaptchaForm()


    currency_symbol = get_setting("site", "global", "currencysymbol")
    if not currency_symbol: currency_symbol = "$"

    return render_to_response(template_name, {
        'form':form,
        'captcha_form' : captcha_form,
        'use_captcha' : use_captcha,
        'currency_symbol': currency_symbol},
        context_instance=RequestContext(request))


def add_confirm(request, id, template_name="sponsorships/add_confirm.html"):
    sponsorship = get_object_or_404(Sponsorship, pk=id)
    EventLog.objects.log(instance=sponsorship)
    return render_to_response(template_name, context_instance=RequestContext(request))


@login_required
def detail(request, id=None, template_name="sponsorships/view.html"):
    sponsorship = get_object_or_404(Sponsorship, pk=id)
    if not has_perm(request.user,'sponsorships.view_sponsorship'): raise Http403

    EventLog.objects.log(instance=sponsorship)

    sponsorship.sponsorship_amount = tcurrency(sponsorship.sponsorship_amount)
    return render_to_response(template_name, {'sponsorship':sponsorship},
        context_instance=RequestContext(request))


def receipt(request, id, guid, template_name="sponsorships/receipt.html"):
    sponsorship = get_object_or_404(Sponsorship, pk=id, guid=guid)

    sponsorship.sponsorship_amount = tcurrency(sponsorship.sponsorship_amount)

    EventLog.objects.log(instance=sponsorship)

    if (not sponsorship.invoice) or sponsorship.invoice.balance > 0 or (not sponsorship.invoice.is_tendered):
        template_name="sponsorships/view.html"
    return render_to_response(template_name, {'sponsorship':sponsorship},
        context_instance=RequestContext(request))


@login_required
def search(request, template_name="sponsorships/search.html"):
    query = request.GET.get('q', None)
    if get_setting('site', 'global', 'searchindex') and query:
        sponsorships = Sponsorship.objects.search(query)
    else:
        sponsorships = Sponsorship.objects.all()

    EventLog.objects.log()

    return render_to_response(template_name, {'sponsorships':sponsorships},
        context_instance=RequestContext(request))
