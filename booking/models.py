from django.db import models
from userside.models import *
from adminside.models import *

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_cost = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.user.email} - {self.car.product_name} ({self.start_date} to {self.end_date})"