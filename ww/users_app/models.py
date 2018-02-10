from django.contrib.auth.models import User
from django.db import models
from django.apps.config import MODELS_MODULE_NAME
from datetime import datetime

class Tag(models.Model):
    name = models.CharField(max_length = 80, primary_key = True)
    description = models.CharField(
        max_length = 150,
        blank = True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class Location(models.Model):
    line1 = models.CharField(
        max_length = 150,
        blank = True)
    line2 = models.CharField(
        max_length = 150,
        blank = True)
    line3 = models.CharField(
        max_length = 150,
        blank = True)
    city = models.CharField(
        max_length = 80,
        blank = True)
    state = models.CharField(
        max_length = 80,
        blank = True)
    country = models.CharField(
        max_length = 80,
        blank = True)
    postal_code = models.CharField(
        max_length = 80,
        blank = True)
    longitude = models.FloatField(default = 0, blank = True)
    latitude = models.FloatField(default=0, blank = True)
    created_at = models.DateTimeField(default = datetime.now)
    updated_at = models.DateTimeField(default = datetime.now)
    
# Create your models here.
class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length = 150)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="tag", blank=True)
    location = models.ManyToManyField(Location, related_name="location", blank=True)
    approvals = models.ManyToManyField(User, related_name="user_approvals", blank = True)
    disapprovals = models.ManyToManyField(User, related_name="user_disapprovals", blank = True)
    disable_comments = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField() 
     
class Package(models.Model):
    name = models.CharField(max_length=75)
    description = models.CharField(max_length=300)
    story = models.ForeignKey(Story, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    
class Comment(models.Model):
    story = models.ForeignKey(Story, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    
class Item(models.Model):
    name = models.CharField(max_length = 80)
    description = models.CharField(
        max_length = 150,
        blank = True)
    story = models.ForeignKey(Story, related_name= 'items', on_delete=models.DO_NOTHING) # This is Django's alternative to OneToMany relationship
    source_url = models.CharField(
        max_length = 150,
        blank = True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    

    
     
        
         
