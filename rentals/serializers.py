from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from adminside.serializers import CarsSerializer
from .models import * 
from userside.serializers import UserSerializer

class BookingSerilaizer(ModelSerializer):
    class Meta:
        model = Bookings
        fields = ['id','car', 'user', 'start_date', 'end_date', 'start_time', 'total_cost','booking_status','is_paid']
        
class BookingLists(ModelSerializer):
    car = CarsSerializer()
    user = UserSerializer()
    class Meta:
        model = Bookings
        fields = '__all__'
        
class ReviewCreateSerializer(ModelSerializer):
    class Meta:
     model = Reviews    
     fields = ['user','car', 'booking', 'comment', 'rating']
     
class ReviewListSerializer(ModelSerializer):
    user = UserSerializer()
    car = CarsSerializer()
    class Meta:
        model = Reviews
        fields = '__all__'
        

class CreateOrderSerializer(serializers.Serializer):
        amount = serializers.IntegerField()
        currency = serializers.CharField()

class TransactionModelSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["payment_id", "order_id", "signature","amount"]
