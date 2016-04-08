# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import check_password
from registration.models import CustomUser

class EmailAuthBackend(object):
    """
    A custom authentication backend. Allows users to log in using their email address.
    """

    def authenticate(self, email=None, password=None):
        """
        Authentication method
        """
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except CustomUser.DoesNotExist:
            return None
        
    """def has_perm(self, user_obj, perm, obj=None):
        if user_obj.username == settings.ADMIN_LOGIN:
            return True
        else:
            return False"""