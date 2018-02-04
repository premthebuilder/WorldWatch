from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from .serializers import StorySerializer, TagSerializer
from django.contrib.auth import authenticate


class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        print("hello world")
        self.factory = RequestFactory()
#         self.user = User.objects.get(id=1)

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/customer/details')
        
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
#         request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        request.user = authenticate(username="aster", password = "Vangaurd3515")
        data = {
        "title": "titletest",
        "text": "test",
        "tags":[],
        "approval_ids": [],
        "disapproval_ids":[]
        }
#         data = {
#           "name" : "tag1"  
#         }
#         serializer = StorySerializer(data=data)
        serializer = StorySerializer(context = {'request':request}, data = data)
#         serializer = TagSerializer(data=data)
        print(serializer.is_valid())
        ss = serializer.save()
        
#         self.assertEqual(response.status_code, 200)