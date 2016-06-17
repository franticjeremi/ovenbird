# -*- coding: utf-8 -*-

'''
Created on 6 мая 2016 г.

@author: gudach
'''

from django.db import models
from django_comments.models import CommentAbstractModel, BaseCommentAbstractModel
from django_comments.managers import CommentManager
from django.utils import timezone

from django.conf import settings

COMMENT_MAX_LENGTH = getattr(settings, 'COMMENT_MAX_LENGTH', 3000)

class CommentWithOvenbird(BaseCommentAbstractModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name="%(class)s_comments",
        on_delete=models.SET_NULL
    )
    user_name = models.CharField(
        max_length=100, 
        blank=True
    )
    comment = models.TextField(max_length=COMMENT_MAX_LENGTH)
    
    submit_date = models.DateTimeField(
        default=None, 
        db_index=True
    )
    ip_address = models.GenericIPAddressField(
        unpack_ipv4=True, 
        blank=True, 
        null=True
    )
    is_public = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    # Manager
    objects = CommentManager()
    
    class Meta:
        ordering = ('submit_date',)
        permissions = [("can_moderate", "Can moderate comments")]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        
    def __str__(self):
        return "%s: %s..." % (self.name, self.comment[:50])

    def save(self, *args, **kwargs):
        if self.submit_date is None:
            self.submit_date = timezone.now()
        super(CommentWithOvenbird, self).save(*args, **kwargs)

    def _get_name(self):
        return self.user_name

    def _set_name(self, val):
        if self.user_id:
            raise AttributeError(_("This comment was posted by an authenticated "
                                   "user and thus the name is read-only."))
        self.user_name = val

    name = property(_get_name, _set_name, doc="The name of the user who posted this comment")  