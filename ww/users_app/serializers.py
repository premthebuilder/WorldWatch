from datetime import datetime
from wsgiref import validate

from django.contrib.auth import get_user_model, get_user
from django.template.defaultfilters import default
from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import NOT_READ_ONLY_WRITE_ONLY

from .models import Story, Item


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    def create(self, validated_data):
        print("In create")
        user = get_user_model().objects.create(
                username = validated_data['username']
            )
        user.set_password(validated_data['password'])
        user.email = validated_data['email'] if 'email' in validated_data else None
        user.first_name = validated_data['first_name'] if 'first_name' in validated_data else None
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'first_name')
   
class ItemSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        read_only = True,
        default=serializers.CreateOnlyDefault(timezone.now)
        )
    updated_at = serializers.DateTimeField(
        read_only = True,
        default=serializers.CreateOnlyDefault(timezone.now)
        )
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',)
             
class StorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    approval_ids = serializers.PrimaryKeyRelatedField(many=True, 
                                                   read_only=False, 
                                                   queryset=get_user_model().objects.all(), 
                                                   source='approvals')
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField(
        read_only = True,
        default=serializers.CreateOnlyDefault(timezone.now)
        )
    updated_at = serializers.DateTimeField(
        read_only = True,
        default=serializers.CreateOnlyDefault(timezone.now)
        )
    class Meta:
        model = Story
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',)
        