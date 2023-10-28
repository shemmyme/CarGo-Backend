from django.urls import path
from . import views

urlpatterns = [
    path('car-booking/', views.CarBooking.as_view()),
    path('profile/bookings',views.BookingList.as_view()),
    path('profile/bookings/<int:id>',views.Booking.as_view()),
    # path('profile/bookings/<int:id>', views.BookingUpdateStatus.as_view(), name='update-booking-status')
    path('profile/bookings/<int:id>/cancel', views.CancelBookingView.as_view(), name='booking-cancel'),
    path('reviews/create', views.ReviewCreate.as_view(), name='review-create'),
    path('reviews/list/<int:carId>/', views.ReviewList.as_view(), name='review-list'),
    # path('reviews/list/<int:userId>/', views.UserReview.as_view(), name='review-list'),
    path('reviews/list/', views.ReviewsHome.as_view(), name='review-list'),
    path("order/create/<int:user_id>/",views.CreateOrderAPIView.as_view(), name="create-order-api"),
    path("order/complete/<int:user_id>/",views.TransactionAPIView, name="complete-order-api"),


]
