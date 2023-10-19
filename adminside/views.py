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
    
    def create(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

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
            # Assuming you have a `bookings` relationship field in your Cars model
            # This filters out cars with bookings that overlap with the specified date range
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
    
        
