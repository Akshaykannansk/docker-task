from django.db import models
from apps.authentication.models import CustomUser
from apps.home.models import Product


# Create your models here.
class cart(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE, related_name='cart')
    is_paid = models.BooleanField(default=False)
    total = models.DecimalField(default=0, decimal_places=2, max_digits=6)
 

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        carttotal= sum([cart_item.get_product_price() for cart_item in cart_items])
        self.total= carttotal
        self.save()
        return carttotal
    
   
class CartItems(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE, related_name='cart_items')
    product =models.ForeignKey(Product, on_delete=models.SET_NULL , null=True , blank=True)
    quantity = models.IntegerField(default=1)
    

    def get_product_price(self):
        price = [self.product.price * self.quantity]
        return sum(price)
    
    




    

    