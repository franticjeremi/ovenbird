# -*- coding: utf-8 -*-
from django.test import TestCase, RequestFactory
from django_webtest import WebTest
from .models import Ovenbird, Object, Region, City
from registration.models import CustomUser
from .views import UpdateObject


# Create your tests here.
def create_ovenbird(name, city, telephone, text, customeruser):
    return Ovenbird.objects.create(name=name, city_id=city, 
        telephone=telephone, text=text, customuser_id=customeruser)

def create_object(title, text, price, type, ovenbird):
    return Object.objects.create(title=title, text=text, price=price, type=type, ovenbird=ovenbird)

def create_city(name, region):
    return City.objects.create(name=name, region=region)

def create_region(name):
    return Region.objects.create(name=name)

def create_user(password, email):
    return CustomUser.objects.create(password=password, email=email)

class FormTest(WebTest):
    def setUp(self):
        self.factory = RequestFactory()
        self.region = create_region('Карелия')
        self.city = create_city('ПТЗ', self.region)
        self.user = create_user('top_secret', 'asd@asd')
        self.ovenbird = create_ovenbird('Илья', self.city.id, '324343242', 'sdfdd', self.user.id)
        self.object = create_object('dd','sdfds', 123, 1, self.ovenbird)

    def test_check_work_update_object(self):
        request = self.factory.get('/offsite/Object/Update/%d/' % self.object.id)
        request.user = self.user
        request.ovenbird = self.ovenbird
        request.object = self.object
        request.session = {}
        request.session['ovenbird_id'] = self.ovenbird.id
        response = UpdateObject.as_view()(request, pk = self.object.id)
        self.assertEqual(response.status_code, 200)