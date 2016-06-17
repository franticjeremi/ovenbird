# -*- coding: utf-8 -*-

'''
Created on 6 мая 2016 г.

@author: gudach
'''

from django import forms
from django_comments.forms import CommentForm, CommentSecurityForm
from .models import CommentWithOvenbird
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text
from django.utils import timezone
from django.utils.text import get_text_list
from django.conf import settings
from . import get_model

COMMENT_MAX_LENGTH = getattr(settings, 'COMMENT_MAX_LENGTH', 3000)

class CommentFormWithOvenbird(CommentSecurityForm):
    name = forms.CharField(max_length=100)
    comment = forms.CharField(widget=forms.Textarea,
                              max_length=COMMENT_MAX_LENGTH)
    
    def get_comment_object(self):
        """
        Return a new (unsaved) comment object based on the information in this
        form. Assumes that the form is already validated and will throw a
        ValueError if not.

        Does not set any of the fields that would come from a Request object
        (i.e. ``user`` or ``ip_address``).
        """
        if not self.is_valid():
            raise ValueError("get_comment_object may only be called on valid forms")

        CommentWithOvenbird = self.get_comment_model()
        new = CommentWithOvenbird(**self.get_comment_create_data())
        new = self.check_for_duplicate_comment(new)

        return new

    def get_comment_model(self):
        """
        Get the comment model to create with this form. Subclasses in custom
        comment apps should override this, get_comment_create_data, and perhaps
        check_for_duplicate_comment to provide custom comment models.
        """
        return get_model()

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        return dict(
            content_type=ContentType.objects.get_for_model(self.target_object),
            object_pk=force_text(self.target_object._get_pk_val()),
            user_name=self.cleaned_data["name"],
            comment=self.cleaned_data["comment"],
            submit_date=timezone.now(),
            site_id=settings.SITE_ID,
            is_public=True,
            is_removed=False,
        )

    def check_for_duplicate_comment(self, new):
        """
        Check that a submitted comment isn't a duplicate. This might be caused
        by someone posting a comment twice. If it is a dup, silently return the *previous* comment.
        """
        possible_duplicates = self.get_comment_model()._default_manager.using(
            self.target_object._state.db
        ).filter(
            content_type=new.content_type,
            object_pk=new.object_pk,
            user_name=new.user_name,
        )
        for old in possible_duplicates:
            if old.submit_date.date() == new.submit_date.date() and old.comment == new.comment:
                return old

        return new

    def clean_comment(self):
        """
        If COMMENTS_ALLOW_PROFANITIES is False, check that the comment doesn't
        contain anything in PROFANITIES_LIST.
        """
        comment = self.cleaned_data["comment"]
        if (not getattr(settings, 'COMMENTS_ALLOW_PROFANITIES', False) and
                getattr(settings, 'PROFANITIES_LIST', False)):
            bad_words = [w for w in settings.PROFANITIES_LIST if w in comment.lower()]
            if bad_words:
                raise forms.ValidationError(
                    "Watch your mouth! The word %s is not allowed here.",
                    "Watch your mouth! The words %s are not allowed here.",
                    len(bad_words) % get_text_list(
                    ['"%s%s%s"' % (i[0], '-' * (len(i) - 2), i[-1])
                     for i in bad_words], 'and'))
        return comment