from django.db import models
from apps.authentication.models import CustomUser
from apps.home.models import Product

# Create your models here.
class cart(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE, related_name='cart')
    is_paid = models.BooleanField(default=False)

class CartItems(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE, related_name='cart_items')
    product =models.ForeignKey(Product, on_delete=models.SET_NULL , null=True , blank=True)

    