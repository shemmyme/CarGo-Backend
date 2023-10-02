from django.db import models

# Create your models here.
class Cars(models.Model):
    product_name = models.CharField(max_length=250,unique=True)
    model = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    fuel = models.CharField(max_length=10,null=True)
    rent_amount = models.IntegerField()
    is_available = models.BooleanField(default=True)
    image_1 = models.ImageField(blank=False)
    image_2 = models.ImageField(blank=True)
    image_3 = models.ImageField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    

    
