from .models import *
from rest_framework import serializers
from userside.serializers import *
from rest_framework.serializers import SerializerMethodField


class MessageSerializer(serializers.ModelSerializer):
    sender_username=SerializerMethodField()

    class Meta:
        model=Messages
        fields=['message','sender_username']

    def get_sender_username(self,obj):
        return obj.sender.username

class ChatListSerializer(serializers.ModelSerializer):

    user_profile=SerializerMethodField
    username=SerializerMethodField

    class Meta:
        model=Messages
        fields=['user_profile','username']

    def get_username(self,obj):
        return obj
    
    def get_user_profile(self,obj):
        return UserSerializer(User.objects.filter(user__username=obj).first()).data.get('pic')

