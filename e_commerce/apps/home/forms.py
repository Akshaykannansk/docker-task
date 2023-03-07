from django import forms
from .models import Product,product_category

class ProductForm(forms.ModelForm):
        product_category = forms.ModelChoiceField(queryset=product_category.objects.all(), empty_label=None)
        
        class Meta:
            model = Product
            fields = ['name', 'description', 'price','image','product_category','stock']
            widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
            'category': forms.ModelChoiceField(queryset=product_category.objects.all())
        }
class productCategory(forms.ModelForm):

      
    category_name = forms.CharField(  widget=forms.TextInput(
            attrs={
        
                "class": "form-control"
            }
        ))
    class Meta:
        model = product_category
        fields = ['category_name']