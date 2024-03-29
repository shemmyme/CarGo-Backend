from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# from rentals.models import Bookings
from .models import *

class AccountManger(BaseUserManager):
    def _create_user(self,email,password,**extra_fields):
       if not email:
            raise ValueError('Your have not provided a valid e-mail address')
       
       email=self.normalize_email(email)
       user=self.model(email=email,**extra_fields)
       user.set_password(password)
       user.save(using=self._db)
       return user
    

    def create_user(self, email=None, password=None, **extra_fields):
      
        return self._create_user(email, password, **extra_fields)
        
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=250)
    email = models.EmailField(unique=True)  
    profile_img = models.ImageField(upload_to="profile", blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    licenseFront = models.ImageField(blank=True)
    licenseBack = models.ImageField(blank=True)   
    livePhoto = models.ImageField(blank=True) 
    is_verified = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects=AccountManger()


    def __str__(self):
        return self.email 
    
    def has_perm(self,pars,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True
    
    
# 
      