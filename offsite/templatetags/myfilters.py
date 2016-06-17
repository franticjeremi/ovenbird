# encoding: utf-8

from django import template 

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.group.filter(name=group_name).exists()