from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect
from django.views import View
from apps.home.models import Product
from shop.models import CartItems , cart
from django.shortcuts import render, get_object_or_404



# Create your views here.
class shop(View):
    template_name = 'shop/product_list.html'
    context = {}

    def get(self, request):
        product = Product.objects.all()
        context ={
            'products':product
        }
        return render(request,self.template_name,context)




def add_to_cart(request,id):
    products = Product.objects.get(id=id)
    user = request.user
    print(user,products,"========================================================================"
    )
    Cart , _ = cart.objects.get_or_create(user=user,is_paid= False)
    cart_item = CartItems.objects.create(product=products,cart=Cart)
    Cart.save()
    cart_item.save()
    from django.urls import reverse
    return HttpResponseRedirect(reverse("product_detail"))



def product_detail(request, id):
    products = Product.objects.get(id=id)
    context = {'product': products}
    return render(request, 'shop/product_detail.html', context)