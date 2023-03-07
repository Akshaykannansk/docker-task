from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect
from django.views import View
from apps.home.models import Product
from shop.models import CartItems , cart ,Orders,Order_items
from django.shortcuts import render, get_object_or_404
from shop.forms import address_form



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
    cart_items = user_cart.items.all()
    total_price = user_cart.get_cart_total()
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'shop/cart.html', context)


class checkout(View):
    template_name ='shop/checkout.html'
    context = {}

    def get(self, request, *args, **kwargs):
        context = {
            'form' : address_form()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
         form = address_form(request.POST)
         if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            total1 = cart.objects.filter(user=request.user).values_list('total', flat=True).first()


            order = Orders.objects.create(user=request.user, address=address , total = total1 )
            if request.user.cart:
                cart_id = request.user.cart.values('id').first()['id']
                cart_items = CartItems.objects.filter(cart_id = cart_id).all()
                product = Product.objects.all()
                for item in cart_items:
                    product = Product.objects.filter(id=item.product_id).first()
                    Order_items.objects.create(order=order, product=product.name, quantity=item.quantity, price=item.get_product_price())
                cart_items.delete()
                product.stock -= item.quantity
                product.save()
         return render(request, 'shop/checkout_success.html', {'order': order})
    



   
