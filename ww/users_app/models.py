from django.db import models
from django.contrib.auth import User
from django.contrib.gis.gdal.field import Field



# Create your models here.

class Story(models.Model):
    author = models.ManyToManyField(User)
    title = models.CharField(max_length = 150)
    text = models.TextField()
    approvals = models.IntegerField(blank=True)
    disapprovals = models.IntegerField(blank=True)
    disable_comments = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField() 
     
class Package(models.Model):
    name = models.CharField(max_length=75)
    description = models.CharField(max_length=300)
    story = models.ForeignKey(Story)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    
class Comment(models.Model):
    story = models.ForeignKey(Story)
    author = models.ForeignKey(User)
    text = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    
    
class Tag(models.Model):
    name = models.CharField(max_length = 80)
    description = models.CharField(
        max_length = 150,
        blank = True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    
class Item(models.Model):
    name = models.CharField(max_length = 80)
    description = models.CharField(
        max_length = 150,
        blank = True)
    package = models.ForeignKey(Package)
    source_url = models.CharField(
        max_length = 150,
        blank = True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
class Location(model.Model):
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
    gps_location = models.CharField(
        max_length = 80,
        blank = True)
    
     
        
         
