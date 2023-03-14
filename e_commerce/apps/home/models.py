# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from apps.authentication.models import CustomUser


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

  




