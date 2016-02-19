# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from unittest.mock import DEFAULT
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
    is_admin = models.BooleanField(default=False)
    is_ovenbird = models.BooleanField(default=False)
    is_adser = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Пользователь"
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []