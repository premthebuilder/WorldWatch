import django
from django.conf import settings
settings.configure()
django.setup()


import serializers

data = {
        "title": "titletest",
        "text": "test",
        "tags":["tag1"],
        "approval_ids": [],
        "disapproval_ids":[]
    }
serializer = serializers.StorySerializer(data = data)
serializer.is_valid()