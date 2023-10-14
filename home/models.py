from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import User

default_value = timezone.now


# Create your models here.
CATEGORY_CHOICES=(
    ('Py','Python'),
    ('HT','HTML'),
    ('CS','CSS'),
    ('JS','Javascript'),
    ('BS','Bootstrap'),
    ('CW','C'),
    ('CC','C++'),
    ('JA','Java'),
)
STATE_CHOICES=(
    ('TN','TamilNadu'),

)

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='product')  # You can specify a different upload path if needed
    vendor = models.CharField(max_length=20)
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    discount_price = models.FloatField(blank=False, default=0.0)
    selling_price = models.FloatField(blank=False, default=0.0)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title

class Customer(models. Model):
    user = models. ForeignKey (User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField (max_length=200)
    city = models.CharField (max_length=50)
    mobile = models. IntegerField(default=0)
    zipcode = models. IntegerField()
    state = models.CharField (choices=STATE_CHOICES,max_length=100)
    def __str_(self):
        return self.name
class Cart (models. Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey (Product, on_delete=models. CASCADE)
    quantity = models.PositiveIntegerField (default=1)
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price


STATUS_CHOICES =(
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
    )



class Payment (models. Model):
    user = models. ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField (max_length=100, blank=True,null=True)
    razorpay_payment_status = models.CharField (max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField (max_length=100, blank=True,null=True)
    paid = models. BooleanField (default=False)

class OrderPlaced (models. Model):
    user = models. ForeignKey(User,on_delete=models.CASCADE)
    customer = models. ForeignKey(Customer, on_delete=models. CASCADE)
    product = models. ForeignKey(Product, on_delete=models. CASCADE)
    quantity = models. PositiveIntegerField(default=1)
    ordered_date= models.DateTimeField(auto_now_add=True)
    status = models. CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models. ForeignKey(Payment,on_delete=models.CASCADE, default="")

    @property
    def total_cost (self):
        return self.quantity * self.product.discount_price
