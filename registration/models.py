# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group
from offsite.models import Ovenbird
import logging
logger = logging.getLogger(__name__)

class UserFullName(Ovenbird):
    class Meta:
        proxy = True

    def __str__(self):
        return self.get_full_name() or 'Anonymous'


class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_staff=True,
            is_active=True,
            is_superuser=True
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

# Create your models here.
class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True,
        default = 'nobody',
        verbose_name = "Электронная почта"
    )
    joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    group = models.ManyToManyField(
        Group,
        blank=True,
    )
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def get_full_name(self):
        # The user is identified by their email address
        return UserFullName.objects.get(customuser_id=self.id)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email
    
    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_group(self, group):
        # Simplest possible answer: Yes, always
        return self.groups.filter(name=group).exists()