# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse         
from apps.authentication.models import CustomUser
from django.views.generic import View
from django.views import View
from .forms import ProductForm
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .models import Product
from wallet.models import UserWallet


@login_required(login_url="/login/")
def index(request):
    user = UserWallet.objects.get(user=request.user)
    context = {'segment': 'index', 'balance': user.balance}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


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
            CustomUser.objects.filter(id__in=user_ids).update(is_active=False)
        elif action == 'unblock':
            CustomUser.objects.filter(id__in=user_id).update(is_active=True)
        # Redirect back to the user list
        return redirect('userlist')
    
    else:
        active = CustomUser.objects.filter(is_active= True)
        blocked = CustomUser.objects.filter(is_active= False)
        context = {'active': active,'blocked': blocked, 'segments':'userlist'}    
        return render(request, 'home/user_list.html', context)










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




class ProductView(TemplateView):
    template_name = 'home/view_product.html'
    context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mydata = Product.objects.all().values()
        context['product'] = mydata
        return context


def delete(request, id):
  
  Product = Product.objects.get(id=id)
  Product.delete()
  return HttpResponseRedirect(reverse('product_view'))

 
def update(request, id):
  Products = Product.objects.get(id=id)
  template = loader.get_template('update.html')
  context = {
    'Product': Products,
  }
  return HttpResponse(template.render(context, request))

  
def updaterecord(request, id):
  name = request.POST['name']
  description = request.POST['description']
  price = request.POST['price']
  image = request.POST['image']
  member = Product.objects.get(id=id)
  member.name = name
  member.price = price
  member.image = image
  member.save()
  return HttpResponseRedirect(reverse('index'))
