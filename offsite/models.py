from django.db import models
import os
from django.db.models.fields.related import ForeignKey

def get_upload_path(instance, filename):
    return os.path.join("ovenbird_%d/%s" % (instance.ovenbird.id, filename))

def get_upload_path_ads(instance, filename):
    return os.path.join("adser_%d/%s" % (instance.adser.id, filename))

# create path to image file for current user
class Photo(models.Model):
    ovenbird = models.ForeignKey('Ovenbird')
    object = models.ManyToManyField('Object')
    description = models.TextField(
        null=True, 
        blank=True
    )
    date_created = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to=get_upload_path)
    
    def __str__(self):
        return '%s' % (self.image)

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
    main_photo = models.ForeignKey(
        Photo,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='main_photo'
    )
    
class Adser(models.Model):
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0
    )
    customuser = models.OneToOneField('registration.CustomUser', default=0)
    
class Video(models.Model):
    ovenbird = models.ForeignKey('Ovenbird')
    object = models.ForeignKey('Object')
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    embed = models.CharField(max_length=255)

# imagine name for class
class Object(models.Model):
    ovenbird = models.ForeignKey('Ovenbird')
    title = models.CharField(max_length=200)
    text = models.TextField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True
    )
    type = models.PositiveSmallIntegerField()
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    title_photo = models.ForeignKey(
        Photo,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='title_photo'
    )
    object_link = models.ManyToManyField('Object')
    filter_link = models.ManyToManyField('Filter')
    
class Region(models.Model):
    name = models.CharField(max_length=70)
    
    def __str__(self):
        return '%s' % (self.name)
    
class City(models.Model):
    name = models.CharField(max_length=50)
    region = models.ForeignKey('Region')
    
    def __str__(self):
        return '%s' % (self.name)
    
class Ads(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=get_upload_path_ads)
    date_start = models.DateField(
        blank=True,
        null=True
    )
    date_end = models.DateField(
        blank=True,
        null=True
    )
    link = models.CharField(
        max_length=200, 
        blank=True,
        null=True
    )
    #region = models.ForeignKey('Region')
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0
    )
    is_payed = models.CharField(
        max_length=1,
        default = 'N'
    )
    filter_link = models.ManyToManyField('Filter')
    adser = models.ForeignKey('Adser')
    
    
class Filter(models.Model):
    title = models.CharField(max_length=200)
    filter_link = models.ManyToManyField(
        'Filter',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return '%s' % (self.title)