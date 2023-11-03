from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .serializers import UserSerializer,UserRegisterSerializer
from .models import User
from django.http import HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from adminside.serializers import CarsSerializer
from adminside.models import Cars
from rest_framework import viewsets
from django.http import Http404
from django.http import JsonResponse






class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['is_admin'] = user.is_admin   
        token['id'] = user.id
        token['is_verified'] = user.is_verified
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer 
        
    
@api_view(['GET'])
def Activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        print('saved')

        return HttpResponseRedirect('https://cargoself.vercel.app/login')
        
    
    
class UserRegistration(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(password)
            user.save()

            # Get the user's ID
            user_id = user.id
            print(user_id,'usersrsrsrsrrs ididididid')

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('account_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'cite': current_site
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            response_data = {
                'status': 'success',
                'msg': 'A verification link sent to your registered email address',
                'data': {
                    'id': user_id, 
                },
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'msg': serializer.errors})

      
@api_view(["GET"])
def getRoutes(request):
    routes = [
        "api/login",
        # "api/token/refresh",
    ]
    return Response(routes)

@receiver(post_save, sender=User)
def send_email_to_admin(sender, instance, created, **kwargs):
    if created and (instance.licenseFront or instance.licenseBack):
        subject = "User Uploaded License Photo"
        message = f"User {instance.username} (ID: {instance.id}) has uploaded a license photo."
        from_email = "cargo.rentals123@gmail.com"
        recipient_list = ["shemim313@gmail.com"]

        send_mail(subject, message, from_email, recipient_list)


# ////////////////////////////////////////////////////////////////////////////////////////////


@api_view(['GET'])
def UserProfileView(request,user_id):
    user = get_object_or_404(User,id = user_id)
    
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['PATCH'])
def UpdateUserProfile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("User not found")

    print(f"user_id from token: {user_id}")

    # Handle licenseFront and licenseBack file uploads
    license_front = request.FILES.get('licenseFront')
    license_back = request.FILES.get('licenseBack')
    live_photo = request.FILES.get('livePhoto')  # Handle livePhoto file upload
    if license_front:
        user.licenseFront = license_front
    if license_back:
        user.licenseBack = license_back
    if live_photo:
        user.livePhoto = live_photo  # Update the livePhoto field
        print(live_photo)

    new_username = request.data.get('username')
    profile_img = request.FILES.get('profile_img')
    
    if new_username:
        user.username = new_username
        
    if profile_img:
        user.profile_img = profile_img

    user.save()
    
    
    

    # Trigger the signal after saving the user
    if (license_front or license_back or live_photo):
        post_save.send(sender=User, instance=user, created=True)

    return Response({"message": "Changes updated successfully"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def block_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = False  # Deactivate the user
        user.save()
        return JsonResponse({'message': 'User blocked successfully'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
@api_view(['POST'])
def unblock_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True  # Activate the user
        user.save()
        return JsonResponse({'message': 'User unblocked successfully'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@api_view(['PATCH'])
def verify_user(request, userId):
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    print(user,'nokkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
    if user:
        user.is_verified = True  # Set the user as verified
        user.save()
        print('aaaaaaaaayiiiiiiiiiiiiiiiii')
        return Response({"message": "User has been verified"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET'])
def car_detail(request, carId):
    car = get_object_or_404(Cars, id=carId)
    serializer = CarsSerializer(car)
    return Response(serializer.data)


    
@api_view(['GET'])
def UserView(request,user_id):
    user = get_object_or_404(User,id = user_id)
    
    serializer = UserSerializer(user)
    
    response_data={
        'user':serializer.data
    }
    return Response(response_data)

def get_user_data(request):
    users = User.objects.values('id', 'username')  # You can customize the fields you need
    return JsonResponse(list(users), safe=False)

def get_queryset(self):
        # Get a list of user IDs from the query parameters
        user_ids = self.request.query_params.get('ids', '').split(',')

        # Filter the User queryset based on the provided user IDs
        return User.objects.filter(id__in=user_ids)

