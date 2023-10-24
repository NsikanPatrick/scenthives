from django.db import models
from django.contrib.auth.models import User
from django.db import models
import random
import string
import time
import uuid
from shop.models import Perfume

# Create your models here.
class Order(models.Model):
    PENDING = 'pending'
    PROCESSING = 'processing'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    SHIPPED = 'shipped'


    STATUS_CHOICHES = (
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled')
    )
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100 , null=False)
    email = models.EmailField(max_length=100 , null=False)
    country = models.CharField(max_length=100 , null=False)
    city = models.CharField(max_length=100 , null=False)
    state = models.CharField(max_length=100 , null=False)
    additional_info = models.TextField(null=False)
    address = models.TextField()
    zipcode = models.CharField(max_length=100)
    # phone = models.IntegerField()
    phone = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_number = models.CharField(max_length=25, null=True, unique=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    #payment_mode = models.CharField(max_length=250)
    reference = models.CharField(max_length=50)
    #payment_gateway_token = models.CharField(max_length=250)
    is_completed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICHES, default=PENDING)

    class Meta:
        ordering = ['-created_at',]
    
    def __str__(self):
        return self.first_name
    
    def generate_order_number(self):
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        timestamps = int(time.time() * 1000)
        return f"AUX-{random_chars}-{timestamps}"
        #order_number = f"AUX-{random_chars}-{timestamps}"
        #self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    perfume = models.ForeignKey(Perfume, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    #sub_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '%s' % self.id
