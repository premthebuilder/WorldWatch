from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import urls
from rest_framework import routers
from users_app.views import (StoryViewSet, 
    CreateUserViewSet, CreateStoryViewSet, get_upload_session_url)
from rest_framework_jwt.views import obtain_jwt_token

router = routers.DefaultRouter()
router.register(r'story', StoryViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^register/$', CreateUserViewSet.as_view(), name='user'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^new_story/', CreateStoryViewSet.as_view(), name='story'),
    url(r'^upload_session_url/', get_upload_session_url, name="upload_url"),
]
