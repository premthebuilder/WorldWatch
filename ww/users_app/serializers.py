from rest_framework import serializers
from .models import Story
from rest_framework.fields import NOT_READ_ONLY_WRITE_ONLY
from django.contrib.auth import get_user_model, get_user
from wsgiref import validate
from datetime import datetime
from django.utils import timezone
from django.template.defaultfilters import default
        
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
        
class StorySerializer(serializers.ModelSerializer):
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
    approvals = serializers.IntegerField(
        default=serializers.CreateOnlyDefault(0))
    disapprovals = serializers.IntegerField(
        default=serializers.CreateOnlyDefault(0))
    class Meta:
        model = Story
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',)
         
#     def create(self, validated_data):
#         print("Creating a new story")
#         user = None
#         request = self.context.get("request")
#         if request and hasattr(request, "user"):
#             user = request.user
#             story = Story.objects.create(**validated_data)
# #             story = Story(
# #                 author = [user],
# #                 title = validated_data.get('title'),
# #                 text = validated_data.get('text'),
# #                 approvals = 0,
# #                 disapprovals = 0,
# #                 disable_comments = validated_data.get('disable_comments', False),
# #                 created_at = datetime.now())
#             story.save(
#                 author = user,
#                 title = validated_data.get('title'),
#                 text = validated_data.get('text'),
#                 approvals = 0,
#                 disapprovals = 0,
#                 disable_comments = validated_data.get('disable_comments', False),
#                 created_at = datetime.now()
#                 )
#             return story