from rest_framework import serializers
from .models import *

class CarsSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Cars
        fields = '__all__'
        
class CouponsSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Coupons
        fields = '__all__'
