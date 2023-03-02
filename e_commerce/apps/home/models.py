# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class product_category(models.Model):
    category_name = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.category_name 
    
    @staticmethod
    def get_all_categories():
        return product_category.objects.all() 


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True)
    product_category = models.ForeignKey(product_category, on_delete=models.CASCADE)


    def __str__(self):
        return self.name   
    
    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter (id__in=ids)
    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter (category=category_id)
        else:
            return Product.get_all_products()
