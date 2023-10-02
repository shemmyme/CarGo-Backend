# serializers.py
from rest_framework import serializers
from .models import *
    
class BookingSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Booking
        fields = '__all__'
