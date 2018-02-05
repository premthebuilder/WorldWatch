from datetime import datetime
from wsgiref import validate

from django.contrib.auth import get_user_model, get_user
from django.template.defaultfilters import default
from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import NOT_READ_ONLY_WRITE_ONLY
import logging
from logging.config import _handle_existing_loggers
logger = logging.getLogger(__name__)

try:
    from .models import Story, Item, Tag, Location
except Exception:
    from models import Story, Item, Tag, Location

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
        
class LocationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        read_only = True,
        default=serializers.CreateOnlyDefault(timezone.now)
        )
    updated_at = serializers.DateTimeField(
        read_only = True,
        default=serializers.CreateOnlyDefault(timezone.now)
        )
    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',)
        
class TagSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(TagSerializer, self).__init__(many=many, *args, **kwargs)
    created_at = serializers.DateTimeField(
        read_only = True,
        default=serializers.CreateOnlyDefault(timezone.now)
        )
    updated_at = serializers.DateTimeField(
        read_only = True,
        default=serializers.CreateOnlyDefault(timezone.now)
        )
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',)
        
    def create(self, validated_data):
        instance, _ = Tag.objects.get_or_create(**validated_data)
        return instance
             
class StorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    approval_ids = serializers.PrimaryKeyRelatedField(many=True, 
                                                   read_only=False, 
                                                   queryset=get_user_model().objects.all(), 
                                                   source='approvals')
    disapproval_ids = serializers.PrimaryKeyRelatedField(many=True, 
                                                   read_only=False, 
                                                   queryset=get_user_model().objects.all(), 
                                                   source='disapprovals')
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
    
#     def create(self, validated_data):
#         tags_data = validated_data.pop('tags')
#         story = Story.objects.create(**validated_data)
#         for tag in tags_data:
#             tag_data = {"name": tag_name}
#             tag_obj, created = Tag.objects.get_or_create(**tag_data)
#             story.tags.add(tag_obj)
#         story.save()
#         return story
    
if __name__ == "__main__":
    data = {
        "title": "titletest",
        "text": "test",
    }
    serializer = StorySerializer(data = data)
    serializer.is_valid()
        