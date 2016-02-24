from django.db import models
import os
from django.conf import settings

class Ovenbird(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(
        'City',
        null=True,
        blank=True
    )
    telephone = models.CharField(
        max_length=13,
        null=True,
        blank=True
    )
    text = models.TextField(null=True, blank=True)
    customuser = models.OneToOneField('registration.CustomUser', default=0)
    #photo = ImageField
    
class Adser(models.Model):
    balance = models.DecimalField(max_digits=10, 
        decimal_places=2,
        default=0
    )
    customuser = models.OneToOneField('registration.CustomUser', default=0)

def get_upload_path(instance, filename):
    return os.path.join(settings.MEDIA_ROOT, "ovenbird_%d/object_%d/%s" % (instance.ovenbird.id, instance.object.id, filename))

# create path to image file for current user
class Photography(models.Model):
    ovenbird = models.ForeignKey('Ovenbird')
    object = models.ForeignKey('Object')
    title = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    description = models.TextField(
        null=True, 
        blank=True
    )
    date_created = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to=get_upload_path)
    
class Video(models.Model):
    ovenbird = models.ForeignKey('Ovenbird')
    object = models.ForeignKey('Object')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to=get_upload_path)

# imagine name for class
class Object(models.Model):
    ovenbird = models.ForeignKey('Ovenbird')
    title = models.CharField(max_length=200)
    text = models.TextField()
    price = models.DecimalField(max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True
    )
    type = models.PositiveSmallIntegerField()
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    
class Region(models.Model):
    name = models.CharField(max_length=70)
    
    def __str__(self):
        return '%s' % (self.name)
    
class City(models.Model):
    name = models.CharField(max_length=50)
    region = models.ForeignKey('Region')
    
    def __str__(self):
        return '%s' % (self.name)