# -*- coding: utf-8 -*-
'''
Created on 16 июня 2016 г.

@author: gudach
'''
from django.http import JsonResponse

class Base(object):
    def __init__(self, email, password, token=None):
        self.email = email
        self.password = password
        self._response = None
        self._token = '9e3b1bff710f0e7329368cb752f5d91d24a4a9a6a8c06300ef8b0d94b2eb033006dd279d9061d1b8b6ade'

    @property
    def response(self):
        return self._response
        
    
