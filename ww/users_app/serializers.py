from rest_framework import serializers
from .models import Story
from rest_framework.fields import NOT_READ_ONLY_WRITE_ONLY
from django.contrib.auth import get_user_model, get_user

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ('id', 'author', 'title', 'text')
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    def create(self, validated_data):
        print("In create")
        user = get_user_model().objects.create(
                username = validated_data['username']
            )
        user.set_password(validated_data['password'])
        user.email = validated_data['email'] if validated_data.has_key('email') else None
        user.first_name = validated_data['first_name'] if validated_data.has_key('first_name') else None
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'first_name')