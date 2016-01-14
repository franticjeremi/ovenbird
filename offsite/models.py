from django.db import models

# Create your models here.
class ovenbird(models.Model):
    name = models.CharField(max_length=200)
    city_id = models.IntegerField()
    telephone = models.CharField(max_length=12)
    email = models.EmailField(max_length=254)
    text = models.TextField()
    #photo = ImageField

#class adser(models.Model):
#    name = models.CharField(max_length=200)

class photo(models.Model):
    ovenbird_id = models.ForeignKey('ovenbird')
    name = models.CharField(max_length=200)
    description = models.TextField()
    #photo = ImageField