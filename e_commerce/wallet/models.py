from django.db import models
from apps.authentication.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class UserWallet(models.Model) :
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=7, decimal_places=2 ,default=0.00)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserWallet.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.userwallet.save()
    

#     ---------------------------------------------------------------- coupon ----------------------------------------------
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateField()
    is_expired = models.BooleanField(default=False)