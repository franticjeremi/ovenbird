# -*- coding: utf-8 -*-
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import Ovenbird, Object, Region, City
from registration.models import CustomUser
from .views import UpdateObject

from django.test import Client
client = Client()

# Create your tests here.
def create_ovenbird(name, city, telephone, text, customeruser):
    return Ovenbird.objects.create(name=name, city=city, 
        telephone=telephone, text=text, customuser=customeruser)

def create_object(title, text, price, type, ovenbird):
    return Object.objects.create(title=title, text=text, price=price, type=type, ovenbird=ovenbird)

def create_city(name, region):
    return City.objects.create(name=name, region=region)

def create_region(name):
    return Region.objects.create(name=name)

def create_user(password, email):
    return CustomUser.objects.create(password=password, email=email)

class FormTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.region = create_region('Карелия')
        self.city = create_city('ПТЗ', self.region)
        self.user = create_user('top_secret', 'asd@asd')
        self.ovenbird = create_ovenbird('Илья', self.city, '324343242', 'sdfdd', self.user)
        self.object = create_object('dd','sdfds', 123, 1, self.ovenbird)

    def test_check_work_update_object(self):
        request = self.factory.get('/offsite/UpdateObject/%s/' % self.object.id)
        request.user = self.user
        request.ovenbird = self.ovenbird
        request.object = self.object
        # Test my_view() as if it were deployed at /customer/details
        #response = my_view(request)
        # Use this syntax for class-based views.
        response = UpdateObject.as_view()(request)
        self.assertEqual(response.status_code, 200)