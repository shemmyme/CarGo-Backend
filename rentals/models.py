from django.db import models
from userside.models import User
from adminside.models import Cars
import string
from datetime import datetime
import random

def generate_order_id():
    """Generate a 14-character order ID"""
    while True:
        letters = string.ascii_uppercase + string.digits
        order_id = ''.join(random.choice(letters) for i in range(9))
        year = str(datetime.now().year)[-2:]
        month = str(datetime.now().month)[-2:]
        day = str(datetime.now().day)
        hour = str(datetime.now().hour)
        new_id = 'BNB' + year + month + day + hour+ order_id
        return new_id

class Bookings(models.Model):
    
    STATUS_CHOICES =[
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
        ('Rented', 'Rented'),
        ('Returned', 'Returned'),
        ('available', 'available')
    ]
    
    # booking_id = models.CharField(max_length=20, null=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    total_cost = models.IntegerField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    booking_status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='available')  
    is_paid = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"Booking for {self.user.email} - {self.car.product_name} ({self.start_date} to {self.end_date})"

class Reviews(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      car = models.ForeignKey(Cars,on_delete=models.CASCADE)
      booking = models.ForeignKey(Bookings,on_delete=models.CASCADE)
      comment = models.CharField(max_length=255)
      rating = models.IntegerField(default=0)
      
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Bookings,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, verbose_name="Payment ID")
    order_id = models.CharField(max_length=100, verbose_name="Order ID")
    signature = models.CharField(max_length=200, verbose_name="Signature")
    amount = models.IntegerField(verbose_name="Amount")
    datetime = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return(self.id)