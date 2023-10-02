from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('signup/', views.UserRegistration.as_view()),
    path('', views.getRoutes, name='get_routes'),
    path('profile/<int:user_id>/', views.UserProfileView, name='profile-view'),
    path('profileup/<int:user_id>/', views.UpdateUserProfile, name='profile-update'),
    path('verify/<int:userId>/', views.verify_user, name='verify-license'),
    path('login/',views. MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('activate/<uidb64>/<token> ', views.Activate, name='activate'),
    path('cars/<int:carId>/', views.car_detail, name='car_detail'),
    
]
