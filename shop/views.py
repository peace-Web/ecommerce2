from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import datetime
import json
from .utils import cookieCart
from django.contrib.auth.models import User, auth
from django.contrib import messages
# Create your views here.

def store(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user = request.user).first()
        order, created = Order.objects.get_or_create(complete = False, customer = customer)
        items = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        items = cookieData["items"]
        order = cookieData["order"]
    context = {"products": products, "items": items, "order":order}
    return render(request, 'shop/store.html', context)

def view(request, pk):
    product = Product.objects.get(id = pk)
    context = {"product": product}
    return render(request, 'shop/view.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user = request.user).first()
        order, created = Order.objects.get_or_create(complete = False, customer = customer)
        items = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        items = cookieData["items"]
        order = cookieData["order"]
        # cartItems = cookieData["cartItems"]
    context = {"items": items, "order":order}
    return render(request, 'shop/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user = request.user).first()
        order, created = Order.objects.get_or_create(complete = False, customer = customer)
        items = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        items = cookieData["items"]
        order = cookieData["order"]
        cartItems = cookieData["cartItems"]
    context = {"items": items, "order":order}
    return render(request, 'shop/checkout.html', context)

def updateitem(request):
    product_id = request.POST["product_id"]
    action = request.POST["action"]
    print("id: "+product_id)
    print("action: "+action)
    customer = request.user.customer
    product = Product.objects.get(id = product_id)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderitem, created = OrderItem.objects.get_or_create(order = order, product = product )

    if action == "Add":
        orderitem.quantity += 1
    elif action == "Remove":
        orderitem.quantity -= 1
    
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()
    
    
    return JsonResponse("item was added", safe=False)

def proccessOrder(request):
    transation_id = datetime.datetime.now().timestamp()
    total = float(request.POST["total"])
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        
        print(float(total))
        print(float(order.total_order))

        

    else:
        print("User not logged in...")
        print("Cookies", request.COOKIES)
        name = request.POST["name"]
        email = request.POST["email"]
        cookieData = cookieCart(request)
        items = cookieData["items"]

        customer, created = Customer.objects.get_or_create(email = email)
        customer.name = name
        customer.save()

        order = Order.objects.create(
            customer = customer,
            complete = False
        )
        for item in items:
            product = Product.objects.get(id = item["product"]["id"])

            orderItem = OrderItem.objects.create(
                product = product,
                order = order,
                quantity = item["quantity"]
            )
    
    if total == float(order.total_order):
        order.transactio_id = transation_id
        order.complete = True
        print("True")
    order.save()
    if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                city = request.POST["city"],
                address = request.POST["address"],
                zipcode = request.POST["zipcode"],
            )
    return JsonResponse("order complete", safe=False)

def logoutPage(request):
    auth.logout(request)
    return redirect('login')


def loginPage(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user =  auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.warning("credentials are not valid! try again")
            return redirect("login")
    return render(request, 'shop/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST["name"]
        email = request.POST["email"]
        password1 = request.POST["password"]
        password2 = request.POST["confirm-password"]
        if password1 == password2:
            if User.objects.filter(username = username).exists():
               messages.warning(request, 'This username is already exists! try an other one please.')
               return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.warning(request, 'This email is already exists! try an other one please.')
                return redirect('register')
            else:
                user = User.objects.create_user(username= username, email= email, password= password1)
                user.save()
                messages.info(request, 'Your account created successfully.')
                return redirect('login')
        else:
            messages.warning(request, 'Passwords are identical! try again please')
            return redirect('register')
    

    else:
      return render(request, 'shop/register.html')