from .models import Story
from .serializers import StorySerializer, UserSerializer
from .google_cloud_client import GoogleStoreClient

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

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
    
def get_upload_session_url(request):
    client = GoogleStoreClient("yuga-171020.appspot.com")       
    response_json = {"upload_session_url" : client.create_upload_session_url()}
    return JsonResponse(response_json)

    
# class ExceptionLoggingMiddleware(object):
#     def process_request(self, request):
#         print(request.body)
#         print(request.scheme)
#         print(request.method)
#         print(request.META)
#         return None