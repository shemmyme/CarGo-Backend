from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Booking
from .serializer import BookingSerializer

# Import necessary modules
from datetime import date
from decimal import Decimal

# Define your custom function to calculate the total cost
def calculate_total_cost(car_id, start_date, end_date):
    
    daily_rate = Decimal('50.00')  # Replace with your actual daily rate
    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)
    number_of_days = (end_date - start_date).days + 1
    total_cost = daily_rate * Decimal(str(number_of_days))
    
    return total_cost


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            print(user,'user aaraaaaaaaaaaaa')
            car_id = serializer.validated_data['carId']
            print(car_id,'carid aaraaaaaaaaaaaaaaaaa')
            start_date = serializer.validated_data['startDate']
            end_date = serializer.validated_data['endDate']

            # Calculate the total cost here as needed
            total_cost = calculate_total_cost(car_id, start_date, end_date)

            # Create a booking
            booking = Booking.objects.create(
                user=user,
                car_id=car_id,
                start_date=start_date,
                end_date=end_date,
                total_cost=total_cost  # Store the calculated total cost
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)