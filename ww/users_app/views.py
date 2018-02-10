from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.decorators import permission_classes
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .gcs_signed_url import CloudStorageURLSigner
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from . import util


import base64
import datetime
import hashlib
import sys
import time

import Crypto.Hash.SHA256 as SHA256
import Crypto.PublicKey.RSA as RSA
import Crypto.Signature.PKCS1_v1_5 as PKCS1_v1_5
import requests
from . import conf
from django_filters.rest_framework.backends import DjangoFilterBackend
# try:
#   import conf
# except ImportError:
#   sys.exit('Configuration module not found. You must create a conf.py file. '
#            'See the example in conf.example.py.')

# The Google Cloud Storage API endpoint. You should not need to change this.
GCS_API_ENDPOINT = 'https://storage.googleapis.com'

# from .google_cloud_client import GoogleStoreClient
from .models import Story, Item, Tag
from .serializers import (StorySerializer,
                           UserSerializer,
                           ItemSerializer,
                           TagSerializer,
                           LocationSerializer)


class StoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ['title', 'text', 'tags__name']
    ordering = ['title', 'text']
    queryset = Story.objects.all().order_by('created_at')
    serializer_class = StorySerializer
    
class TagViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    model = Tag
    serializer_class = TagSerializer
    
class CreateUserViewSet(CreateAPIView):
#     renderer_classes = (JSONRenderer,)
    model = get_user_model()
    permission_classes(AllowAny)
    serializer_class = UserSerializer
    
class CreateStoryViewSet(CreateAPIView):
    model = Story
    permission_classes = (AllowAny,) #TODO: Change this to IsAuthe
    serializer_class = StorySerializer
    
class CreateItemViewSet(CreateAPIView):
    model = Item
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer
    
# class AddApproval(UpdateAPIView):
#     queryset = Story.objects.all()
#     serializer_class = StorySerializer
#     permission_classes = (IsAuthenticated,)
# 
#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         user_approved = get_user_model().objects.get(pk=request.data.get("new_approval"))
#         instance.approvals.add(user_approved)
#         instance.save()
# 
#         serializer = self.get_serializer(instance)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
# 
#         return Response(serializer.data)

class StoryUpdateView(UpdateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

@api_view(['get'])
@csrf_exempt
def get_current_user(request):
    if request.user:
        return JsonResponse({
                "username" : request.user.username,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            })
    else:
        return Response("UserNotLoggedIn", status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@csrf_exempt
def add_story_approval(request):
    if request.user:
        try:
            story_id = request.POST.get("story_id")
            story = Story.objects.get(pk=story_id)
            story.approvals.add(request.user)
            story.save()
            serializer = StorySerializer(story)
            return Response(serializer.data)
        except Exception as e:
            return Response("ErrorFetchingStory: " + str(e), status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("UserNotLoggedIn", status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@csrf_exempt
def create_story_with_tags(request):
    if request.user:
        try:
            request.POST._mutable = True
            tags_data = request.data.pop("tags")[0] if "tags" in request.data else ""
            latitude = request.data.pop("latitude")[0] if "latitude" in request.data else None
            longitude = request.data.pop("longitude")[0] if "longitude" in request.data else None
            location_data = {}
            if latitude and longitude:
                location_data = {"latitude": float(latitude), "longitude": float(longitude)}
            tags_data = tags_data.split(",")
            story_serializer = StorySerializer(context = {'request':request}, data = request.data)
            if story_serializer.is_valid():
                story = story_serializer.save()
                for tag_data in tags_data:
                    if tag_data:
                        tag_serializer = TagSerializer(data={"name": tag_data})
                        if tag_serializer.is_valid():
                            tag = tag_serializer.save()
                            story.tags.add(tag)
                story.save()
                if location_data:
                    location_serializer = LocationSerializer(data=location_data)
                    if location_serializer.is_valid():
                        location = location_serializer.save()
                        story.location.add(location)
                        story.save()
                    
                return Response(story_serializer.data)
        except Exception as e:
            return Response("ErrorCreatingStory: " + str(e), status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("UserNotLoggedIn", status=status.HTTP_401_UNAUTHORIZED)      
                
@api_view(['POST'])
@csrf_exempt
def get_upload_session_url(request):
    image_md5 = request.POST.get("md5")
    object_name = util.generate_uuid() + ".jpg"
    if image_md5:
        try:
          keytext = open(conf.PRIVATE_KEY_PATH, 'rb').read()
        except IOError as e:
          sys.exit('Error while reading private key: %s' % e)
        
        private_key = RSA.importKey(keytext)
        signer = CloudStorageURLSigner(private_key, conf.SERVICE_ACCOUNT_EMAIL,
                                       GCS_API_ENDPOINT)
        file_path = '/%s/%s' % (conf.BUCKET_NAME, object_name)
        put_request = signer.GeneratePutUrl(file_path, 'image/jpeg', image_md5)
        response_json = {"upload_session_url" : put_request}
        return JsonResponse(response_json)
    
    
@api_view(['POST'])
@csrf_exempt
def get_download_session_url(request):
    object_name = request.POST.get("objectName")
    try:
      keytext = open(conf.PRIVATE_KEY_PATH, 'rb').read()
    except IOError as e:
      sys.exit('Error while reading private key: %s' % e)
    
    private_key = RSA.importKey(keytext)
    signer = CloudStorageURLSigner(private_key, conf.SERVICE_ACCOUNT_EMAIL,
                                   GCS_API_ENDPOINT)
    file_path = '/%s/%s' % (conf.BUCKET_NAME, object_name)
    put_request = signer.GenerateGetUrl(file_path)
    response_json = {"download_session_url" : put_request}
    return JsonResponse(response_json)


#     client = GoogleStoreClient("yuga-171020.appspot.com")       
#     response_json = {"upload_session_url" : client.create_upload_session_url()}
#     return JsonResponse(response_json)

    
# class ExceptionLoggingMiddleware(object):
#     def process_request(self, request):
#         print(request.body)
#         print(request.scheme)
#         print(request.method)
#         print(request.META)
#         return None