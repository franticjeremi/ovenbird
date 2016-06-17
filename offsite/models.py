# -*- coding: utf-8 -*-
from django.db import models
import os
from django.db.models.fields.related import ForeignKey
from mptt.models import MPTTModel, TreeForeignKey
from vote.managers import VotableManager
from django.conf import settings

def get_upload_path(instance, filename):
    return os.path.join("ovenbird_%d/photo/%s" % (instance.customuser.id, filename))

def get_upload_path_ads(instance, filename):
    return os.path.join("ovenbird_%d/ads/%s" % (instance.customuser.id, filename))

# create path to image file for current user
class Photo(models.Model):
    customuser = models.ForeignKey(settings.AUTH_USER_MODEL)
    object = models.ManyToManyField('Object')
    description = models.TextField(
        null=True, 
        blank=True
    )
    date_created = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to=get_upload_path)
    
    def __str__(self):
        return '%s' % (self.image)
    
    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

class Ovenbird(models.Model):
    name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    location = models.ForeignKey(
        'Location',
        null=True,
        blank=True
    )
    telephone = models.CharField(
        max_length=13,
        null=True,
        blank=True
    )
    text = models.TextField(
        null=True, 
        blank=True
    )
    customuser = models.OneToOneField(settings.AUTH_USER_MODEL, default=0)
    main_photo = models.ForeignKey(
        Photo,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='main_photo'
    )
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0
    )
    
    class Meta:
        verbose_name = "Печник"
        verbose_name_plural = "Печники"
        
    def get_full_name(self):
        # The user is identified by their email address
        return self.name
    
class Video(models.Model):
    customuser = models.ForeignKey(settings.AUTH_USER_MODEL)
    object = models.ForeignKey('Object')
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    embed = models.CharField(max_length=255)

# объекты, статьи, товары, заявки
class Object(models.Model):
    customuser = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200)
    text = models.TextField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True
    )
    type = models.PositiveSmallIntegerField(db_index=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    title_photo = models.ForeignKey(
        Photo,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='title_photo'
    )
    filter_link = models.ManyToManyField('Filter')
    votes = VotableManager()
    
    class Meta:
        verbose_name = "Объект/Статья"
        verbose_name_plural = "Объекты/Статьи"

class Location(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="children",
        db_index=True
    )
    
    def __str__(self):
        return '%s' % (self.name)
    
    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"
    
    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']
    
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
    #location = models.ForeignKey('Location')
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0
    )
    is_payed = models.BooleanField(default = False)
    auto_payment = models.BooleanField(default = True)
    filter_link = models.ManyToManyField('Filter')
    customuser = models.ForeignKey(settings.AUTH_USER_MODEL)
    location = models.ForeignKey(
        'Location',
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = "Реклама"
        verbose_name_plural = "Реклама"
    
    
class Filter(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="children",
        db_index=True
    )
    
    def __str__(self):
        return '%s' % (self.name)
    
    class Meta:
        verbose_name = "Фильтр"
        verbose_name_plural = "Фильтры"
        
    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']
    