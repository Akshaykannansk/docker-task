# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from apps.authentication.models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.


class product_category(models.Model):
    category_name = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.category_name 
    
   

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(max_length = 50 ,default=1) 
    image = models.ImageField(upload_to='images/', blank=True)
    product_category = models.ForeignKey(product_category, on_delete=models.CASCADE)


class bonushistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_bonuses')
    sponsor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sponsor_bonuses')
    bonusesamount = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(default=datetime.now)

class profile(models.Model):

    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address = models.CharField(max_length=50 , null=True )
    city = models.CharField(max_length=50 , null=True )
    pincode = models.CharField(max_length=6 , null=True )
    country = models.CharField(max_length=50 , null=True )
    AboutMe = models.CharField(max_length=100 , null=True )
  


    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile.objects.create(user=instance)

    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save() 




