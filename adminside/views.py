# views.py
from .models import *
from userside.models import User
from .serializers import *
from userside.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status, generics
from django.db.models import Q
from django.contrib import messages
from rest_framework.decorators import api_view
from django.utils import timezone
from django.http import JsonResponse



class CarAddView(generics.CreateAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
    
    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(request.data,'reqqqqqqqqqqqqqqqst')
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CouponAddView(generics.CreateAPIView):
    queryset = Coupons.objects.all()
    serializer_class = CouponsSerialzer
    
    def create(self, request, *args, **kwargs):
        coupon_code = request.data.get('coupon_code', '')  # Get the name of the coupon from the request data
        existing_coupon = Coupons.objects.filter(coupon_code=coupon_code).first()
        
        if existing_coupon:
            # A coupon with the same name already exists
            messages.error(request, f"A coupon with the name '{coupon_code}' already exists.")
            return Response({"detail": "Coupon with the same name already exists."}, status=status.HTTP_208_ALREADY_REPORTED)

        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CouponListView(generics.ListAPIView):
    serializer_class = CouponsSerialzer
    pagination_class = PageNumberPagination  # Use PageNumberPagination for pagination

    def get_queryset(self):
        queryset = Coupons.objects.all()

        # Search functionality
        search_query = self.request.query_params.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(coupon_code__icontains=search_query)
            )
        
        queryset = queryset.order_by('-created_at')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CarListView(generics.ListAPIView):
    serializer_class = CarsSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Cars.objects.all()

        # Search functionality
        search_query = self.request.query_params.get('search', '')
        if search_query:
            queryset = queryset.filter(Q(product_name__icontains=search_query))

        # Date filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:

            queryset = queryset.exclude(
                bookings__end_date__gte=start_date,
                bookings__start_date__lte=end_date
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CarDeleteView(generics.DestroyAPIView):
    queryset = Cars.objects.all()  
    serializer_class = CarsSerializer
    

    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def list(self,requestm,*args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)

@api_view(['GET'])
def validate_coupon(request, coupon_code):
    user_id = request.GET.get('user_id')

    try:
        now = timezone.now().date()
        coupon = Coupons.objects.get(coupon_code=coupon_code)

        if user_id:
            user = User.objects.get(id=user_id)

            # Check if the user has already used this coupon
            if UserCouponUsage.objects.filter(user=user, coupon=coupon).exists():
                return JsonResponse({'error': 'Coupon already applied by user'}, status=400)

        # Case 1: Coupon code exists, not expired, and uses remaining
        if coupon.start_date <= now <= coupon.end_date and coupon.uses_remaining > 0:
            discount_percentage = coupon.discount_perc
            coupon.uses_remaining -= 1
            coupon.save()

            # If the coupon is successfully applied, add the user to the list of users who have used the coupon
            if user_id:
                UserCouponUsage.objects.create(user=user, coupon=coupon)

            return JsonResponse({'discount_perc': discount_percentage})

        # Case 2: Coupon code exists, but it's expired
        if now < coupon.start_date or now > coupon.end_date:
            return JsonResponse({'error': 'Coupon has expired'}, status=400)

        # Case 3: Coupon code exists, but no uses remaining
        if coupon.uses_remaining <= 0:
            return JsonResponse({'error': 'Coupon has no uses remaining'}, status=400)

    except Coupons.DoesNotExist:
        # Case 4: Coupon code not found
        return JsonResponse({'error': 'Coupon not found'}, status=404)

    # Case 5: Coupon validation failed (for any other error)
    return JsonResponse({'error': 'Coupon validation failed'}, status=500)
