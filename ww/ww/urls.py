from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework import urls
from rest_framework_jwt.views import obtain_jwt_token

from users_app.views import (StoryViewSet,
    CreateUserViewSet, CreateStoryViewSet,
    CreateItemViewSet, StoryUpdateView,
    get_current_user, get_upload_session_url,
    get_download_session_url, add_story_approval,
    create_story_with_tags)

router = routers.DefaultRouter()
router.register(r'story', StoryViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^register/$', CreateUserViewSet.as_view(), name='user'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^create/story/', CreateStoryViewSet.as_view(), name='story'),
    url(r'^create_storytags/', create_story_with_tags, name="create_storytags"),
    url(r'^approve_story/', add_story_approval, name="approve_story"),
    url(r'^get_user_info/', get_current_user, name="user_info"),
    url(r'^create/item/', CreateItemViewSet.as_view(), name="item"),
    url(r'^create/tags/', CreateItemViewSet.as_view(), name="tag"),
    url(r'^view/story/all', StoryViewSet.as_view({'get':'list'}), name="story_list"),
    url(r'^view/story/(?P<pk>[0-9]+)/$', StoryViewSet.as_view({'get':'retrieve'}), name='get_story'),
    url(r'^update/story/(?P<pk>[0-9]+)/$', StoryUpdateView.as_view(), name="story_update"),
    url(r'^upload_session_url/', get_upload_session_url, name="upload_url"),
    url(r'^download_session_url/', get_download_session_url, name="download_url"),
]
