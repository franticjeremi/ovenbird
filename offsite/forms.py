# -*- coding: utf-8 -*-
from django import forms
from offsite.models import Ovenbird, Location, Object, Photo, Ads, Filter
from registration.models import CustomUser
from django.contrib.auth.models import Group
from tinymce.widgets import TinyMCE
import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext as _

from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)

class OvenbirdForm(forms.ModelForm):

    name = forms.CharField(
        label="Имя или организация",
        widget=forms.TextInput
    )
    location = forms.ModelChoiceField(
        label="Город",
        queryset = Location.objects.filter(children__id__isnull=True),
        required=False,
        to_field_name="id"
    )
    telephone = forms.CharField(
        label="Телефон",
        widget=forms.TextInput,
        required=False
    )
    text = forms.CharField(
        label="Информация",
        widget=forms.Textarea,
        required=False,
    )
    customuser = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    group = forms.ModelMultipleChoiceField(
        label="Группы",
        queryset = Group.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Ovenbird
        fields = ['name', 'location', 'telephone', 'text', 'customuser',]
            
    def clean_customuser(self):
        data = CustomUser.objects.get(id=self.cleaned_data['customuser'])
        if not data:
            raise forms.ValidationError()
        return data
            
    def save(self, commit=True):
        user = super(OvenbirdForm, self).save(commit=False)
        if commit:
            user.save()
        return user
            
class ObjectForm(forms.ModelForm):

    title = forms.CharField(
        label="Заголовок",
        widget=forms.TextInput
    )
    text = forms.CharField(
        label="Текст",
        widget=TinyMCE(attrs={'cols': 75, 'rows': 20})
    )
    price = forms.DecimalField(
        label="Цена",
        widget=forms.TextInput,
        required=False
    )
    type = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    customuser = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    filter_link = forms.ModelMultipleChoiceField(
        label="Фильтр",
        required=False,
        widget=Select2MultipleWidget(attrs={'style': 'width:200px'}),
        queryset = Filter.objects.all(),
    )

    class Meta:
        model = Object
        fields = ['title', 'text', 'price', 'type', 'customuser', 'filter_link',]
        
    def __init__(self, *args, **kwargs):
        super(ObjectForm, self).__init__(*args, **kwargs)
        if 'type' in self.initial:
            if self.initial['type'] != 1:
                self.fields['price'].widget = forms.HiddenInput()

    def clean_type(self):
        data = self.cleaned_data['type']
        if not data:
            raise forms.ValidationError()
        return data
    
    def clean_customuser(self):
        data = CustomUser.objects.get(id=self.cleaned_data['customuser'])
        if not data:
            raise forms.ValidationError()
        return data
    
    def save(self, commit=True):
        object = super(ObjectForm, self).save(commit=False)
        if commit:
            object.save()
        return object
    
class FileUploadForm(forms.ModelForm):
    
    customuser = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    object = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )
    description = forms.CharField(
        label="Описание",
        widget=forms.Textarea,
        required = False
    )

    image = forms.ImageField(label="Изображение")
    
    class Meta:
        model = Photo
        fields = ['description', 'image', 'object', 'customuser']
        
    def clean_customuser(self):
        data = CustomUser.objects.get(id=self.cleaned_data['customuser'])
        if not data:
            raise forms.ValidationError()
        return data
   
    def save(self, commit=True):
        object = super(FileUploadForm, self).save(commit=False)
        if commit:
            object.save()
        return object
    
class AdsForm(forms.ModelForm):
    title = forms.CharField(
        label="Заголовок",
        widget=forms.TextInput
    )
    image = forms.ImageField(label="Изображение")
    link = forms.CharField(
        label="Сслыка на сайт",
        widget=forms.TextInput,
        required=False
    )
    customuser = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    auto_payment = forms.BooleanField(
        widget=forms.CheckboxInput(),
        initial = True,
        label="Авто продление оплаты",
    )
    location = forms.ModelChoiceField(
        label="Город",
        queryset = Location.objects.all(),
        required=False,
        to_field_name="id"
    )
    filter_link = forms.ModelMultipleChoiceField(
        label="Фильтр",
        required=False,
        widget=Select2MultipleWidget(attrs={'style': 'width:200px'}),
        queryset = Filter.objects.all(),
    )
    class Meta:
        model = Ads
        fields = ('title', 'image', 'link', 'customuser', 'location', 'filter_link', 'auto_payment',)
        
    def clean_customuser(self):
        data = CustomUser.objects.get(id=self.cleaned_data['customuser'])
        if not data:
            raise forms.ValidationError()
        return data
   
    def save(self, commit=True):
        object = super(AdsForm, self).save(commit=False)
        if commit:
            object.save()
        return object