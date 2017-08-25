from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .gcs_signed_url import CloudStorageURLSigner
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt


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
# try:
#   import conf
# except ImportError:
#   sys.exit('Configuration module not found. You must create a conf.py file. '
#            'See the example in conf.example.py.')

# The Google Cloud Storage API endpoint. You should not need to change this.
GCS_API_ENDPOINT = 'https://storage.googleapis.com'

from .google_cloud_client import GoogleStoreClient
from .models import Story, Item
from .serializers import (StorySerializer,
                           UserSerializer,
                           ItemSerializer)


class StoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Story.objects.all().order_by('created_at')
    serializer_class = StorySerializer
    
class CreateUserViewSet(CreateAPIView):
#     renderer_classes = (JSONRenderer,)
    model = get_user_model()
    permission_classes(AllowAny)
    serializer_class = UserSerializer
    
class CreateStoryViewSet(CreateAPIView):
    model = Story
    permission_classes = (IsAuthenticated,)
    serializer_class = StorySerializer
    
class CreateItemViewSet(CreateAPIView):
    model = Item
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer
    
@api_view(['POST'])
@csrf_exempt
def get_upload_session_url(request):
    image_md5 = request.POST.get("md5")
    if image_md5:
        try:
          keytext = open(conf.PRIVATE_KEY_PATH, 'rb').read()
        except IOError as e:
          sys.exit('Error while reading private key: %s' % e)
        
        private_key = RSA.importKey(keytext)
        signer = CloudStorageURLSigner(private_key, conf.SERVICE_ACCOUNT_EMAIL,
                                       GCS_API_ENDPOINT)
        file_path = '/%s/%s' % (conf.BUCKET_NAME, conf.OBJECT_NAME)
        put_request = signer.GeneratePutUrl(file_path, 'image/jpeg', image_md5)
        response_json = {"upload_session_url" : put_request}
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