from django import forms
from transactions.models import Creditcard

class Credit_card_form(forms.ModelForm):
    class Meta:
        model=Creditcard
        fields=['card_type','amount','name','number','month','year','cvv']

