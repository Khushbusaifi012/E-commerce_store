from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django import forms
from .models import CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Product
from .models import Product, CartItem
from .models import CartItem

# Create your views here.
def home(request):
    return render(request, 'home.html')    #for home file

def about(request):
    return render(request, 'about.html')   #for about file

#signup view
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Something went wrong. Please try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


# LOGIN VIEW
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


#for logout;
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')

#for products
def products(request):
    all_products = Product.objects.all()
    return render(request, 'products.html', {'products': all_products})

#for cart
def cart_view(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        
        # Calculate total per item
        for item in cart_items:
            item.total = item.product.price * item.quantity

        return render(request, 'cart.html', {'cart_items': cart_items})
    else:
        return redirect('login')
    

#for cart item addition;
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

#for cart item update;
@login_required
def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.filter(user=request.user, product=product).first()

    if cart_item and request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save()
    return redirect('cart')

#for checkout;
def checkout(request):
    return render(request, 'checkout.html') 

@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    # Calculate total
    total = 0
    for item in cart_items:
        item.total = item.product.price * item.quantity
        total += item.total

    shipping = 50
    grand_total = total + shipping

    if request.method == 'POST':
        fullname = request.POST['fullname']
        address = request.POST['address']
        city = request.POST['city']
        zipcode = request.POST['zipcode']
        phone = request.POST['phone']
        cardnumber = request.POST['cardnumber']
        expiry = request.POST['expiry']
        cvv = request.POST['cvv']

        # Save Order
        order = Order.objects.create(
            user=request.user,
            full_name=fullname,
            address=address,
            city=city,
            zipcode=zipcode,
            phone=phone,
            card_number=cardnumber,
            expiry=expiry,
            cvv=cvv
        )

        # Save Order Items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        # Clear Cart
        cart_items.delete()

        return redirect('order_success')

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'shipping': shipping,
        'grand_total': grand_total
    })

#for order success;
def order_success(request):
    return render(request, 'order_success.html')
