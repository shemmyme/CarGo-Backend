from django.urls import path
from . import views

urlpatterns = [
    path('addcar/', views.CarAddView.as_view()),
    path('listcar/', views.CarListView.as_view()),
    path('listcar/<int:pk>/', views.CarDeleteView.as_view(), name='car-delete'),
    path('users/', views.UserListView.as_view()),
    path('addcoupon/', views.CouponAddView.as_view()),
    path('listcoupon/', views.CouponListView.as_view()),
     path('validate-coupon/<str:coupon_code>/', views.validate_coupon, name='validate_coupon'),
    
]
