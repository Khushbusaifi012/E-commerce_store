
from django.contrib import admin
from .models import Product
from .models import CartItem
from .models import Order
from .models import OrderItem

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)

