from django.db import models
from apps.authentication.models import CustomUser
from apps.home.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver


class address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    country = models.CharField(max_length=50)
 

# Create your models here.
class cart(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE, related_name='cart')
    is_paid = models.BooleanField(default=False)
    total = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def get_cart_total(self): 
        cart_items = self.items.all()
        carttotal= sum([cart_item.get_product_price() for cart_item in cart_items])
        self.total= carttotal
        self.save()
        return carttotal
   
class CartItems(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE, related_name='items')
    product =models.ForeignKey(Product, on_delete=models.SET_NULL , null=True , blank=True)
    quantity = models.IntegerField(default=1)

    def get_product_price(self):
        price = [self.product.price * self.quantity]
        return sum(price)   



class Orders(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(address, null=True, on_delete=models.SET_NULL)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length= 25, default="pending")
    calculation = models.IntegerField(default=0)



    
class Order_items(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_items')
    product = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)



class bonuses(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,default=0.00 ,null=True)
    badge = models.CharField(max_length=50 , default="nothing" , null=True)

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            bonuses.objects.create(user=instance)

    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.bonuses.save()





    





    

    