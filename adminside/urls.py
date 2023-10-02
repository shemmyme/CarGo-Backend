from django.urls import path
from . import views

urlpatterns = [
    path('addcar/', views.CarAddView.as_view()),
    path('listcar/', views.CarListView.as_view()),
    path('listcar/<int:pk>/', views.CarDeleteView.as_view(), name='car-delete'),
    path('users/', views.UserListView.as_view()),
    
]
