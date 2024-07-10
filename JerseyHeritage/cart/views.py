from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.


def cart_summary(request):
    #get the cart
    cart = Cart(request)
    cart_products = cart.see_products
    
    
    
    return render(request, "cart_summary.html", {"cart_products":cart_products})

def cart_add(request):
    #get the cart
    cart = Cart(request)
    
    if request.POST.get('action') == 'post' :
        #get the product
        product_id = int(request.POST.get('product_id'))
        #look for product
        product = get_object_or_404(Product, id=product_id)
        
        #savr the the add to carts to session
        cart.add(product=product)
        
        cart_quantity = cart.__len__()
        
        #response = JsonResponse({'Product Name:': product.name})

        response = JsonResponse({' qty': cart_quantity})
        return response
        
    
    

def cart_delete(request):
    pass

def cart_update(request):
    pass