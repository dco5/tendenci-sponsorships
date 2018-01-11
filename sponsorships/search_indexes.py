from haystack import indexes

from sponsorships.models import Sponsorship


class SponsorshipIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    sponsorship_amount = indexes.FloatField(model_attr='sponsorship_amount')
    allocation = indexes.CharField(model_attr='allocation')
    payment_method = indexes.CharField(model_attr='payment_method')
    company = indexes.CharField(model_attr='company')
    address = indexes.CharField(model_attr='address')
    city = indexes.CharField(model_attr='city')
    state = indexes.CharField(model_attr='state')
    zip_code = indexes.CharField(model_attr='zip_code')
    email = indexes.CharField(model_attr='email')
    phone = indexes.CharField(model_attr='phone')

    @classmethod
    def get_model(self):
        return Sponsorship

    def get_updated_field(self):
        return 'create_dt'
