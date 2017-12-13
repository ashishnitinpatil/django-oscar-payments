from django import forms
from django.utils.translation import ugettext_lazy as _
from oscar.apps.payment import forms as payment_forms

from oscar_payments.modules.payment.dummy import CREDIT_CARDS


class BankcardForm(payment_forms.BankcardForm):
    """Update the BankcardForm to accept only our test credit cards"""
    card_type = forms.ChoiceField(choices=((cc, cc) for cc in CREDIT_CARDS),
                                  label=_('Card Type'),)

    def __init__(self, *args, **kwargs):
        super(BankcardForm, self).__init__(*args, **kwargs)

        # move the card_type field to the top
        card_type = self.fields.move_to_end('card_type')
        # inefficient hack, can be improved?
        for field in list(self.fields.keys())[:-1]:
            self.fields.move_to_end(field)

        # set up card number help text
        self.fields['number'].help_text = _(
            'Valid numbers: %s') % str(CREDIT_CARDS)

    def clean(self):
        card_type = self.cleaned_data['card_type']
        if not self.cleaned_data['number'] in CREDIT_CARDS[card_type]:
            self._errors['number'] = self.error_class([_("Please enter a valid "
                                                         "credit card number")])
        return self.cleaned_data


BillingAddressForm = payment_forms.BillingAddressForm
