# -*- coding: utf-8 -*-
'''
Created on 16 июня 2016 г.

@author: gudach
'''

class SocialAdapter(object):
    
    def __init__(self, account):
        self.account = account
    
    def send_message(self, user_id=None, message="Test message"):
        self.account.send_message(user_id, message)
        return self.account.response
    
    def get_groups_admin(self, user_id=None):
        self.account.get_groups_admin(user_id)
        return self.account.response
        