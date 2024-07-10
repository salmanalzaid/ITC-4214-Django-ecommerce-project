from .cart import Cart

# to make the cart work on all the pages 
def cart(request):
    return{'cart': Cart(request)}