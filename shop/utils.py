import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES["cart"])
    except:
        cart = {}
    print("Cart", cart)

    items = []
    order = {"total_items": 0, "total_order": 0,"shipping":False}
    cartItems = order["total_items"]
        
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            order["total_items"] += int(cart[i]["quantity"])
            product = Product.objects.get(id = i)
            total = product.price * cart[i]["quantity"]

            order["total_order"] += total
            item = {
                'product': {
                   'id':product.id,
                   'name': product.name,
                   'price': product.price,
                   'digital': product.digital,
                   'imageURL': product.imageURL
                },
                'quantity': cart[i]["quantity"],
                'total': total
            }
            items.append(item)
            if product.digital == False:
                order["shipping"] = True
        except:
            pass
    return {"cartItems": cartItems, "order": order, "items": items}