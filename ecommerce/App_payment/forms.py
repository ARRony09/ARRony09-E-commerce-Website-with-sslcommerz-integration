from django import forms
from .models import Billing_address

class BillingForm(forms.ModelForm):
    class Meta:
        model=Billing_address
        fields=['address','zip_code','city','country']
    