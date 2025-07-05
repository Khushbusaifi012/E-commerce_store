from django.db import models
from django.contrib.auth.models import User


#for add products;
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name


#for add to cart;
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

    
#method to submit order;
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    card_number = models.CharField(max_length=20) 
    expiry = models.CharField(max_length=10)
    cvv = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"



#for order items;;
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):  #method to calculate order item
        return f"{self.product.name} x {self.quantity}"