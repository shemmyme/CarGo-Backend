from django.db import models
from userside.models import User


class Cars(models.Model):
    product_name = models.CharField(max_length=250,unique=True)
    model = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    fuel = models.CharField(max_length=10,null=True)
    rent_amount = models.IntegerField()
    is_available = models.BooleanField(default=True)
    image_1 = models.ImageField(blank=False,upload_to='samples')
    image_2 = models.ImageField(blank=True,upload_to='samples')
    image_3 = models.ImageField(blank=True,upload_to='samples')
    created_date = models.DateTimeField(auto_now_add=True)
    rental_place = models.CharField(max_length=50,null=True)
    
    def __str__(self):
        return self.product_name
    
class Coupons(models.Model):
    coupon_code = models.CharField(max_length=255, unique=True)
    discount_perc = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    uses_remaining = models.PositiveIntegerField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image_1 = models.ImageField(blank=True)
    
class UserCouponUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupons, on_delete=models.CASCADE)
    



    

    
