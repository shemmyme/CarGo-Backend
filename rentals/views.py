from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import date
from rest_framework import filters

 
 
class CarBooking(APIView):
    def post(self, request):
        car = request.data.get('car')
        s_date = request.data.get('start_date')
        e_date = request.data.get('end_date')
        s_time = request.data.get('start_time')
        # e_time = request.data.get('end_time')

        # if Bookings.objects.filter(car__id=car).exists():
        #     vehicle = Bookings.objects.filter(car__id=car)
        #     if vehicle.filter(
        #         (Q(start_date__lte=s_date, end_date__gte=s_date) |
        #         Q(start_date__lte=e_date, end_date__gte=e_date) |
        #         Q(start_date__gte=s_date, end_date__lte=e_date) |
        #         Q(start_date__lte=e_date, end_date__gte=e_date)) & (
        #             Q(booking_status="Pending") | Q(booking_status="Rented"))
        #     ):
        #         return Response(data={'message': 'Slot not available'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookingSerilaizer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # Calculate the current date
            current_date = date.today()
            start_date = date.fromisoformat(s_date)
            end_date = date.fromisoformat(e_date)
            
            serializer.validated_data['booking_status'] = 'Pending'
            serializer.validated_data['is_paid'] = True
            

            if current_date == start_date:
                serializer.validated_data['booking_status'] = 'Rented'

            if current_date > end_date:
                serializer.validated_data['booking_status'] = 'Returned'

            serializer.save()
            return Response(data={'message': 'Booking Success'}, status=status.HTTP_200_OK)

        return Response({'message': 'Some error occurred'}, status=status.HTTP_400_BAD_REQUEST)

class CancelBookingView(generics.DestroyAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerilaizer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user:
            instance.booking_status = 'Cancelled'
            instance.save()
            
            return Response(data={'message': 'Booking canceled successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={'message': 'You are not authorized to cancel this booking'}, status=status.HTTP_403_FORBIDDEN)




class BookingList(generics.ListAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingLists
    
class Booking(generics.RetrieveAPIView):
    queryset = Bookings.objects.all() 
    serializer_class = BookingSerilaizer
    lookup_field = 'id'
    
class ReviewCreate(generics.CreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewCreateSerializer

    
class ReviewsHome(generics.ListAPIView):
    print('reached here')
    queryset = Reviews.objects.all()
    serializer_class = ReviewListSerializer
    print('done all')
    
    
class ReviewList(generics.ListAPIView):
    serializer_class = ReviewListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['car__id']  # Assuming the field is 'car' and its ID is used for filtering

    def get_queryset(self):
        car_id = self.kwargs['carId']
        queryset = Reviews.objects.filter(car=car_id)
        return queryset

# class UserReview(generics.ListAPIView):
#     serializer_class = ReviewListSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['user__id']  # Assuming the field is 'car' and its ID is used for filtering

#     def get_queryset(self):
#         user_id = self.kwargs['userId']
#         queryset = Reviews.objects.filter(user=user_id)
#         return queryset
    
from django.shortcuts import get_object_or_404, render
from django.views import View
from . import client
from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import razorpay
# Create your views here.

class RazorpayClient:
    
    def create_order(self,amount,currency,request):
        car = request.data.get('car')
        s_date = request.data.get('start_date')
        e_date = request.data.get('end_date')
        print(request.data,'request is >>>>>>>>>>>>>>.')        
        if Bookings.objects.filter(car__id=car).exists():
            vehicle = Bookings.objects.filter(car__id=car)
            if vehicle.filter(
                (Q(start_date__lte=s_date, end_date__gte=s_date) |
                Q(start_date__lte=e_date, end_date__gte=e_date) |
                Q(start_date__gte=s_date, end_date__lte=e_date) |
                Q(start_date__lte=e_date, end_date__gte=e_date)) & (
                    Q(booking_status="Pending") | Q(booking_status="Rented"))
            ):
                return Response(data={'message': 'Slot not available'}, status=status.HTTP_400_BAD_REQUEST)
        data = { 
            "amount" : amount * 100,
            "currency" : currency,
        }
        try:
            order_data = client.order.create(data=data)
            return order_data
        except Exception as e:
            raise ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : e
                }
            )
            
    
    def verify_payment(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        try:
            return client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
        except Exception as e:
            raise ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : e
                }
            )


rz_client = RazorpayClient


class CreateOrderAPIView(APIView):
    def post(self, request, user_id):
        try:
            user = get_object_or_404(User, id=user_id)
            create_order_serializer = CreateOrderSerializer(data=request.data)
            if create_order_serializer.is_valid():
                rz_client_instance = RazorpayClient()  
                
                order_response = rz_client_instance.create_order(
                    amount=create_order_serializer.validated_data.get("amount"),
                    currency=create_order_serializer.validated_data.get("currency"),
                    request=request
                )
                response = {
                    "status_code": status.HTTP_201_CREATED,
                    "message": "order created",
                    "data": order_response
                }
                return JsonResponse(response, status=status.HTTP_201_CREATED)

            else:
                print('Ivdee ethiiii >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "error": create_order_serializer.errors
                }
                return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={'message' : 'Slot not avalable'},status=status.HTTP_400_BAD_REQUEST)
        



@api_view(['POST'])
def TransactionAPIView(request,user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        transaction_serializer = TransactionModelSerializer(data=request.data)
        print(user_id,'daxo')
        print(transaction_serializer)
        if transaction_serializer.is_valid():
            
            rz_client = razorpay.Client(auth=("rzp_test_BBvPci4QCLpdZs", "Z8rIFFsHWrBtDmEHi7pnu8uV"))

            
            try:
                rz_client.utility.verify_payment_signature({
                    "razorpay_signature": transaction_serializer.validated_data.get("signature"),
                    "razorpay_payment_id": transaction_serializer.validated_data.get("payment_id"),
                    "razorpay_order_id": transaction_serializer.validated_data.get("order_id"),
                })
            except Exception as e:
                return JsonResponse({
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

            # Save the transaction and update user status
            transaction_serializer.save(user=user)
            user.save()

            return JsonResponse({
                "status_code": status.HTTP_201_CREATED,
                "message": "transaction created"
            }, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": transaction_serializer.errors
            }
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)