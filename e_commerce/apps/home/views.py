# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse         
from apps.authentication.models import CustomUser
from django.views.generic import View, ListView
from django.views import View
from .forms import *
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .models import *
from wallet.models import UserWallet
from shop.models import *
from django.contrib import messages
from django.db.models import Avg, Max, Min, Sum



@method_decorator(login_required(login_url="/login/"), name='dispatch')

class DashBoard(View):
    template_name = 'home/index.html'
    context = {}
    def get(self, request):
        user = UserWallet.objects.get(user=request.user)
        revenue = bonushistory.objects.filter(user_id= request.user).aggregate(Sum('bonusesamount'))
        expense = bonuses.objects.get(user_id= request.user)
        if expense.badge == "Bronze":
            badgeimg = "media/images/vecteezy_winner-glass-award-clipart-design-illustration_9304587_717.png"
        elif expense.badge == "Silver":
            badgeimg = "media/images/vecteezy_winner-glass-award-clipart-design-illustration_9391666_914.png"
        elif expense.badge == "Gold":
            badgeimg = "media/images/vecteezy_winner-glass-award-clipart-design-illustration_9383796_255.png"
        else:
            badgeimg = "media/images/freebadge.png"

        context = {'segment': 'index', 'balance': user.balance,'revenue': revenue, 'expense' : expense, 'badge': badgeimg }
        return render (request, self.template_name, context)

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


#user list printing



# class UserListView(View):
#     def get(request):
#         users = CustomUser.objects.all()
#         context = {'users': users}    
#         return render(request, 'home/user_list.html', context)


@login_required(login_url="/login/")


def UserListView(request):
    if request.method == 'POST':
        # Get the list of user IDs from the form data
        user_ids = request.POST.getlist('user')
        user_id = request.POST.getlist('user1')
        action = request.POST.get('action')
        if action == 'block':
        
        # Deactivate each user with the corresponding ID
            CustomUser.objects.filter(id__in=user_ids).update(is_active=False).exclude(is_superuser= True)
        elif action == 'unblock':
            CustomUser.objects.filter(id__in=user_id).update(is_active=True).exclude(is_superuser= True)
        # Redirect back to the user list
        return redirect('userlist')
    
    else:
        active = CustomUser.objects.filter(is_active= True).exclude(is_superuser= True)
        blocked = CustomUser.objects.filter(is_active= False).exclude(is_superuser= True)
        context = {'active': active,'blocked': blocked, 'segments':'userlist'}    
        return render(request, 'home/user_list.html', context)










@method_decorator(login_required(login_url="/login/"), name='dispatch')
class ProductCategoryAdd(View):
    template_name = 'home/add_product_category.html'
    context = {}
    def get(self, request, *args, **kwargs):
        categories = product_category.objects.all()
        context = {
            'segments':'product category', 
            'categories': categories
            }
        context['form'] = productCategory()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
         categories = product_category.objects.all()
         form = productCategory(request.POST)
         context = {
            'categories': categories,
            'form': form
            }
         if form.is_valid():
            form.save()  # Saves the form data to the database
         return render(request, self.template_name, context )
    
@method_decorator(login_required(login_url="/login/"), name='dispatch')  
class register_product(View):
    template_name = 'home/register_product.html'
    context = {'segments':'register product'}


    def get(self, request, *args, **kwargs):
        self.context['form'] = ProductForm()

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
         form = ProductForm(request.POST, request.FILES)
         print(form,'')
         if form.is_valid():
            form.save()  # Saves the form data to the database
         return render(request, self.template_name, {'form': form})




class ProductView(View):
    template_name = 'home/view_product.html'
    context = {}

    def get(self, request):
        product = Product.objects.all()     
        context ={
            'products':product,
            'segments':'view product'
        }
        return render(request,self.template_name,context)




def delete(request, id):
  del_Product = Product.objects.get(id=id)
  del_Product.delete()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

 
# def update(request, id):
#   Products = Product.objects.get(id=id)
#   context = {
#     'Product': Products,
#   }
#   return render(request, 'home/update.html', context)
    
  
# def updaterecord(request, id):
#   name = request.POST['name']
#   description = request.POST['description']
#   price = request.POST['price']
#   image = request.POST['image']
#   member = Product.objects.get(id=id)
#   member.name = name
#   member.price = price
#   member.image = image
#   member.save()
#   return HttpResponseRedirect(reverse('index'))




class UpdateProductView(View):
    template_name = 'update_product_modal.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = ProductForm(instance=product)
        context = {'form': form, 'product': product}
        return render(request, self.template_name, context)

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
        else:
            messages.error(request, 'Error updating product.')
            context = {'form': form, 'product': product}
            return render(request, self.template_name, context) 



class bonus(View):
    template_name = "home/bonushistory.html"
    context ={}
    def get(self, request):
        bonus = bonushistory.objects.all()       
        userbonus = bonushistory.objects.filter(sponsor_id =request.user)
        context = {
            'bonus' : bonus,
            'userbonus' : userbonus
        }
        return render(request, self.template_name, context)
    

class userprofile(View):
    template_name = "home/profile.html"
    context ={}
    def get(self, request):
        currentuser = CustomUser.objects.get(username = request.user.username)
        aboutme = profile.objects.get(user=request.user)
        user_form = UpdateUserform( instance = request.user)
        profile_form = profileform(instance = request.user.profile)
        context ={
            'userform' : user_form, "profileform":profile_form, 'about':aboutme, 'current_user': currentuser
        }
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
         user_form = UpdateUserform( request.POST, instance = request.user)
         profile_form = profileform(request.POST, instance = request.user.profile)
         currentuser = CustomUser.objects.get(username = request.user.username)
         aboutme = profile.objects.get(user=request.user)
         context ={
            'userform' : user_form, "profileform":profile_form, 'about':aboutme, 'current_user': currentuser
        }
         
         if user_form.is_valid() and profile_form.is_valid():
             user_form.save()
             profile_form.save()
              # Saves the form data to the database
         return render(request, self.template_name, context)
    


class OrderHistoryView (View):
    template_name = "home/orderhistory.html"
    context ={}
    def get(self,request):
        orders = Orders.objects.filter(user_id = request.user)
        ordertotal = orders.aggregate(Sum('total'))
        context = {'order': orders, 'ordertotal': ordertotal}
        return render(request, self.template_name, context)

    
class OrderItemsHistoryView (View):
    template_name = "home/orderitemshistory.html"
    context ={}
    def get(self,request, id):
        orders = Order_items.objects.filter(order_id = id)
        ordertotal = orders.aggregate(Sum('price'))
        context = {'orderitems': orders, 'ordertotal' : ordertotal}
        return render(request, self.template_name, context)
