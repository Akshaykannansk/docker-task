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
    Cart , _ = cart.objects.get_or_create(user=user,is_paid= False)
    cart_item, created = CartItems.objects.get_or_create(product=products, cart=Cart)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def product_detail(request, id):
    products = Product.objects.get(id=id)
    context = {'product': products}
    return render(request, 'shop/product_detail.html', context)


def remove_cart(request, id):
    try:
        cart_item = CartItems.objects.get(product__id=id)
        cart_item.delete()
    except Exception as e:
        print(e)
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def cart_view(request):
    user = request.user
    user_cart = cart.objects.get(user=user)
    cart_items = user_cart.cart_items.all()
    total_price = user_cart.get_cart_total()
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'shop/cart.html', context)

# class checkout(View):
#     template_name ='shop/checkout.html'
#     context = {}

#     def get(self, request):
#         user = request.user
#         user_cart = cart.objects.get(user=user)
#         cart_item = user_cart.cart.objects.all()
#         total_price = user_cart.get_cart_total()
#         context ={
#             'cart':  cart_item,
#             'total_price': total_price
#         }
#         return render(request,self.template_name,context)
