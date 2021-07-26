from store.models import CartLine, Client


def categories_processor(request):
    total = 0
    nb_cart = 0
    if not request.user.is_authenticated:
        if 'cart' in request.session:
            cart = []
            for product_id, quantity in request.session.get('cart').items():
                cart_line = CartLine(product_id=product_id, quantity=quantity)
                total += cart_line.total()
                list.append(cart, cart_line)
                nb_cart = len(cart)
        else:
            cart = None
    else:
        try:
            client = Client.objects.get(user_id=request.user.id)
            cart = CartLine.objects.filter(client_id=client.id)
            for cart_line in cart:
                total += cart_line.total()
            nb_cart = len(cart)
        except:
            cart = None
    return {'cart': cart, 'grand_total': int(total), 'nb_cart': nb_cart}
