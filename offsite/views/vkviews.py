# -*- coding: utf-8 -*-
'''
Created on 15 июня 2016 г.

@author: gudach
'''

from django.http import JsonResponse

from ..providers.vk import Vk


def SendMessage(request):
    myauth = Vk('+79535429588','buzuluk1965')
    myauth.get_groups_admin(350938641)
    data = myauth.response.content
    print(data)
    json = {}
    return JsonResponse(json)