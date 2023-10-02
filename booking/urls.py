
from django.urls import path
from .views import *

urlpatterns = [
    path('cars/<int:carId>/checkout', BookingCreateView.as_view(), name='checkout-api'),
]
