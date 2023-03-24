from django import forms
from .models import cart,CartItems,address

class address_form(forms.ModelForm):
    
    class Meta:
        model = address
        fields = ['first_name', 'last_name', 'address', 'city', 'state', 'pincode', 'country']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }

            
class payment_form(forms.Form):
        CHOICES = [
        (1, 'wallet'),
        (2, 'coupon'),
    ]
        payment_type = forms.ChoiceField(
            widget=forms.RadioSelect,
            choices=CHOICES
        )

class updatecartform(forms.ModelForm):
       quantity = forms.IntegerField

       class Meta:
              model = CartItems
              fields = ['quantity']
       