from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.


def cart_summary(request):
    #get the cart
    cart = Cart(request)
    cart_products = cart.see_products
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    
    
    return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})

def cart_add(request):
    #get the cart
    cart = Cart(request)
    
    if request.POST.get('action') == 'post' :
        #get the product
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #look for product
        product = get_object_or_404(Product, id=product_id)
        
        #savr the the add to carts to session
        cart.add(product=product, quantity= product_qty)
        
        cart_quantity = cart.__len__()
        
        #response = JsonResponse({'Product Name:': product.name})

        response = JsonResponse({' qty': cart_quantity})
        messages.success(request, ("Product added sucessfully !!"))

        return response
        
    
    

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product = product_id)
            
        response = JsonResponse({'product':product_id})
        messages.success(request, ("Your item has been deleted"))

        return response

def cart_update(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		cart.update(product=product_id, quantity=product_qty)

		response = JsonResponse({'qty':product_qty})
		#return redirect('cart_summary')
		messages.success(request, ("Your Cart Has Been Updated..."))
		return response
        
def checkout(request):
    return render(request,"checkout.html")