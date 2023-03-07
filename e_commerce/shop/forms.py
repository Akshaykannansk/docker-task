from django import forms
from .models import cart,CartItems,address

class address_form(forms.ModelForm):
        
        class Meta:
            model = address
            fields = ['first_name', 'last_name', 'address','city','state','pincode','country']
            
