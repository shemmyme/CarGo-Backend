from django.contrib import admin
from django.urls import path,include 

urlpatterns = [
    path('admins/', admin.site.urls),
    path('api/',include('userside.urls')),
    path('admin/',include('adminside.urls')),
]
