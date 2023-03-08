from django import forms
from .models import cart,CartItems,address

class address_form(forms.ModelForm):
        
        class Meta:
            model = address
            fields = ['first_name', 'last_name', 'address','city','state','pincode','country']
            
class payment_form(forms.Form):
        CHOICES = [
        (1, 'wallet'),
        (2, 'coupon'),
    ]
        payment_type = forms.ChoiceField(
            widget=forms.RadioSelect,
            choices=CHOICES, 
        )
