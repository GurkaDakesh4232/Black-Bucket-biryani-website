from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('CB', 'Chicken Biryani'),
    ('MB', 'Mutton Biryani'),
    ('FB', 'Fish Biryani'),
    ('PB', 'Prawns Biryani'),
    ('EB', 'Egg Biryani'),
    ('VB', 'Veg Biryani'),
    ('CC', 'Chicken Curry'),
    ('MC', 'Mutton Curry'),
    ('FPB', 'Fried Piece Biryani'),
]

class Product(models.Model):
    title = models.CharField(max_length=255)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    product_image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    pincode = models.IntegerField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    def __str__(self):
        return f"{self.product.title} in cart of {self.user.username}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    @property
    def total_order_cost(self):
        return sum(item.total_cost for item in self.cart.all())

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
    ('Pending', 'Pending'),
)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)  # Corrected field type
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')  # Correct default value
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)  # Optional field

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
