from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from sponsorships.models import Sponsorship, SponsorshipLevel, NotifyEventAdmin
from sponsorships.utils import get_allocation_choices, get_payment_method_choices, get_preset_amount_choices, \
    get_initial_choice
from tendenci.apps.events.models import Event
from tendenci.apps.site_settings.utils import get_setting

from django.forms.fields import Field
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

setattr(Field, 'is_checkbox', lambda self: isinstance(self.widget, forms.CheckboxInput))

class NotifyEventAdminForm(forms.ModelForm):
    class Meta:
        model = NotifyEventAdmin
        fields = ('notify_emails','event')
    
    def __init__(self, *args, **kwargs):
        super(NotifyEventAdminForm, self).__init__(*args,**kwargs)
        self.fields['event'].widget = forms.HiddenInput()
        self.fields['notify_emails'].help_text = 'Input the list of emails that will be notified on this event. List of eamils must be separate by ",". ' \
                                                ' Example: email1@mail.com, email2@mail.com, email3@mail.com, ....'

    def clean_notify_emails(self):
        # clean_data = super(NotifyEventAdminForm, self).clean()
        clean_data = self.cleaned_data['notify_emails']
        
        if not clean_data:
            self.add_error("Notify emails", 'Emails are needed in this field.')
            raise forms.ValidationError("Error in Emails field!")
        else: 
            emails = clean_data.split(',')
            for email in emails:
                print(email)
                email = email.strip()
                print(email)
                try:
                    validate_email(email)      
                except:
                    self.add_error("Emails List", 'One or more emails in the list are wrong ')
                    raise forms.ValidationError("One or more emails in the list are wrong!")

        return clean_data


class SponsorshipLevelForm(forms.ModelForm):
    class Meta:
        model = SponsorshipLevel
        fields = ('name',
                  'description',
                  'uses_fix_amount',
                  "fix_amount",
                  'min_amount',
                  'max_amount',
                  'limit')

    def __init__(self, *args, **kwargs):
        super(SponsorshipLevelForm, self).__init__(*args, **kwargs)

        self.fields['uses_fix_amount'].help_text = 'Select this if sponsorship level will only use a set amount.'

        self.fields[
            "fix_amount"].help_text = 'If "Uses fix amount" selected, please enter amount for sponsorship level.' \
                                      ' This amount will be ignore if "Uses fix amount" is not selected.'

        self.fields['limit'].help_text = 'Number of sponsors available for this level.'

    def clean(self):
        clean_data = super(SponsorshipLevelForm, self).clean()

        uses_fix_amount = clean_data.get('uses_fix_amount')
        amount = clean_data.get('fix_amount', None)

        if uses_fix_amount and not amount:
            self.add_error("fix_amount", 'Fix Amount cannot be empty if "Uses fix amount" selected.')
            raise forms.ValidationError("Error in Amount field!")

        if not uses_fix_amount:
            min_amount = clean_data.get('min_amount', None)
            max_amount = clean_data.get('max_amount', None)

            if min_amount is None or min_amount <= 0:
                self.add_error('min_amount', 'Please enter correct amount.')
                raise forms.ValidationError("Error with min and max amounts")

            if max_amount is None or max_amount <= 0:
                self.add_error('max_amount', 'Please enter correct amount.')
                raise forms.ValidationError("Error with min and max amounts")

            if min_amount > max_amount:
                self.add_error('min_amount', "Min amount cannot be greater than Max amount.")
                raise forms.ValidationError("Error with min and max amounts")

        return clean_data


class SponsorshipAdminForm(forms.ModelForm):
    # get the payment_method choices from settings
    sponsorship_amount = forms.CharField(error_messages={'required': _('Please enter the sponsorships amount.')})
    payment_method = forms.CharField(error_messages={'required': _('Please select a payment method.')},
                                     widget=forms.RadioSelect(choices=(('check-paid', _('Paid by Check')),
                                                                       ('cc', _('Make Online Payment')),)),
                                     initial='cc', )
    company = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'size': '30'}))
    address = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'size': '35'}))
    state = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'size': '5'}))
    zip_code = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'size': '10'}))
    referral_source = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'size': '40'}))
    email = forms.EmailField(help_text=_('A valid e-mail address, please.'))
    email_receipt = forms.BooleanField(initial=True)
    comments = forms.CharField(max_length=1000, required=False,
                               widget=forms.Textarea(attrs={'rows': '3'}))

    allocation = forms.ChoiceField()

    class Meta:
        model = Sponsorship
        fields = ('sponsorship_amount',
                  'payment_method',
                  'first_name',
                  'last_name',
                  'company',
                  'address',
                  'address2',
                  'city',
                  'state',
                  'zip_code',
                  'phone',
                  'email',
                  'email_receipt',
                  'allocation',
                  'referral_source',
                  'comments',
                  'event',
                  'level'
                  )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user', None)
        else:
            self.user = None
        super(SponsorshipAdminForm, self).__init__(*args, **kwargs)

        preset_amount_str = (get_setting('module', 'sponsorships', 'sponsorshipspresetamounts')).strip('')
        if preset_amount_str:
            self.fields['sponsorship_amount'] = forms.ChoiceField(choices=get_preset_amount_choices(preset_amount_str))

    def clean_sponsorship_amount(self):
        try:
            if float(self.cleaned_data['sponsorship_amount']) <= 0:
                raise forms.ValidationError(_(u'Please enter a positive number'))
        except:
            raise forms.ValidationError(_(u'Please enter a numeric positive number'))
        return self.cleaned_data['sponsorship_amount']


class SponsorshipForm(forms.ModelForm):
    # get the payment_method choices from settings
    payment_method = forms.CharField(error_messages={'required': _('Please select a payment method.')},
                                     widget=forms.RadioSelect(choices=(('check-paid', _('Paid by Check')),
                                                                       ('cc', _('Make Online Payment')),)),
                                     initial='cc', )
    company = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'size': '30'}))
    address = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'size': '35'}))
    state = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'size': '5'}))
    zip_code = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'size': '10'}))
    referral_source = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'size': '40'}))
    email = forms.EmailField(help_text=_('A valid e-mail address, please.'))
    email_receipt = forms.BooleanField(initial=True, required=False)
    comments = forms.CharField(max_length=1000, required=False,
                               widget=forms.Textarea(attrs={'rows': '3'}))

    class Meta:
        model = Sponsorship
        fields = (
            'payment_method',
            'first_name',
            'last_name',
            'company',
            'address',
            'address2',
            'city',
            'state',
            'zip_code',
            'phone',
            'email',
            'email_receipt',
            'referral_source',
            'comments',
            'event',
            'level',
            'sponsorship_amount'

        )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user', None)
        else:
            self.user = None

        if 'event' in kwargs:
            self.event = kwargs.pop('event', None)
        else:
            self.event = None

        super(SponsorshipForm, self).__init__(*args, **kwargs)

        # populate the user fields
        if self.user and self.user.id:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
            try:
                profile = self.user.profile
                if profile:
                    self.fields['company'].initial = profile.company
                    self.fields['address'].initial = profile.address
                    self.fields['address2'].initial = profile.address2
                    self.fields['city'].initial = profile.city
                    self.fields['state'].initial = profile.state
                    self.fields['zip_code'].initial = profile.zipcode
                    self.fields['phone'].initial = profile.phone
            except:
                pass

        self.fields['event'].widget = forms.HiddenInput()
        self.fields['event'].initial = self.event.id

        self.fields['payment_method'].widget = forms.RadioSelect(choices=get_payment_method_choices(self.user))

        self.fields['level'] = forms.ModelChoiceField(
            queryset=SponsorshipLevel.objects.filter(event_id=self.event.id), label="Sponsorship Levels",
            help_text="Please select the level you want to sponsor."
        )

        self.fields['sponsorship_amount'].help_text = 'Please enter appropriate dollar amount for the selected ' \
                                                      'Sponsorship Level.'

    def clean_sponsorship_amount(self):
        # raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))
        try:
            if float(self.cleaned_data['sponsorship_amount']) <= 0:
                self.add_error('sponsorship_amount', 'Please enter a positive number.')
                raise forms.ValidationError(_(u'Please enter a positive number.'))
        except:
            self.add_error('sponsorship_amount', 'Please enter a numeric positive number.')
            raise forms.ValidationError(_(u'Please enter a numeric positive number.'))
        return self.cleaned_data['sponsorship_amount']

    def clean_level(self):
        level = self.cleaned_data['level']
        event_sponsored_levels_count = self.event.sponsorships.filter(level_id=level.id).count()

        if event_sponsored_levels_count >= level.limit:
            self.add_error('level', 'This Sponsorship Level is full, please select another level.')
            raise forms.ValidationError("This Sponsorship Level is full, please select another level.")

        return level

    def clean(self):
        clean_data = super(SponsorshipForm, self).clean()
        level = clean_data.get('level')
        sponsorship_amount = clean_data.get('sponsorship_amount')

        if level.uses_fix_amount:
            if sponsorship_amount != level.fix_amount:
                self.add_error('sponsorship_amount',
                               'Invalid amount for {} level, please enter ${}'.format(level.name, level.fix_amount))
        else:
            if sponsorship_amount < level.min_amount or sponsorship_amount > level.max_amount:
                self.add_error('sponsorship_amount',
                               'Invalid amount for {} level, please enter an amount between ${} and ${}'.format(
                                   level.name,
                                   level.min_amount,
                                   level.max_amount))
        return clean_data

    def save(self, commit=False):
        sponsorship = super(SponsorshipForm, self).save(commit)
        sponsorship.allocation = sponsorship.event.title.strip()
        sponsorship.save()

        return sponsorship


SponsorshipLevelFormSet = inlineformset_factory(Event, SponsorshipLevel, SponsorshipLevelForm, extra=0)
