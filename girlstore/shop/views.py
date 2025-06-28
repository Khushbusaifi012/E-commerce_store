from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Product
from .models import CartItem


# Create your views here.
def home(request):
    return render(request, 'home.html')    #for home file

def about(request):
    return render(request, 'about.html')   #for about file

#login_view
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

# Signup View
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

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
