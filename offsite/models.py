from django.db import models

# Create your models here.
class Ovenbird(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey('City')
    telephone = models.CharField(max_length=13)
    text = models.TextField()
    customuser = models.OneToOneField('registration.CustomUser', default=0)
    #photo = ImageField

#class adser(models.Model):
#    name = models.CharField(max_length=200)

def get_upload_path(instance, filename):
    return "ovenbird_{%s}/{%s}" % (instance.user.id, filename)

# create path to image file for current user
class Photo(models.Model):
    ovenbird = models.ForeignKey('Ovenbird')
    ovenbird = models.ForeignKey('Object')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to=get_upload_path)
    
class Video(models.Model):
    ovenbird = models.ForeignKey('Ovenbird')
    ovenbird = models.ForeignKey('Object')
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
    
class City(models.Model):
    name = models.CharField(max_length=50)
    region = models.ForeignKey('Region')