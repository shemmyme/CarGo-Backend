# views.py
from .models import Cars
from userside.models import User
from .serializers import CarsSerializer
from userside.serializers import UserSerializer
from rest_framework.response import Response
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import status, generics



class CarAddView(generics.CreateAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
    
    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(request.data,'reqqqqqqqqqqqqqqqst')  # Print the request data
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarListView(generics.ListAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
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
    
        
