# -*- coding: utf-8 -*-
from django import forms
from offsite.models import Ovenbird, City, Object, Photo, Ads, Adser
from registration.models import CustomUser
from django.forms.models import formset_factory
from tinymce.widgets import TinyMCE
import logging
logger = logging.getLogger(__name__)

class OvenbirdForm(forms.ModelForm):

    name = forms.CharField(
        label="Имя или организация",
        widget=forms.TextInput
    )
    city = forms.ModelChoiceField(
        label="Город",
        queryset = City.objects.all(),
        required=False,
        to_field_name="id"
    )
    telephone = forms.CharField(
        label="Телефон",
        widget=forms.TextInput
    )
    text = forms.CharField(
        label="Информация",
        widget=forms.Textarea,
        required=False,
    )
    customuser = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Ovenbird
        fields = ['name', 'city', 'telephone', 'text', 'customuser']
        
        
    def __init__(self, *args, **kwargs):
        city = kwargs.pop('city', None)
        super(OvenbirdForm, self).__init__(*args, **kwargs)
        if city:
            self.fields['city'].queryset = City.objects.filter(id=city)
            
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
    ovenbird = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Object
        fields = ['title', 'text', 'price', 'type', 'ovenbird']

    def clean_type(self):
        data = self.cleaned_data['type']
        if not data:
            raise forms.ValidationError()
        return data
    
    def clean_ovenbird(self):
        data = Ovenbird.objects.get(id=self.cleaned_data['ovenbird'])
        if not data:
            raise forms.ValidationError()
        return data
    
    def save(self, commit=True):
        object = super(ObjectForm, self).save(commit=False)
        if commit:
            object.save()
        return object
    
class FileUploadForm(forms.ModelForm):
    
    ovenbird = forms.IntegerField(
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
        fields = ['description', 'image', 'object', 'ovenbird']
        
    def clean_ovenbird(self):
        data = Ovenbird.objects.get(id=self.cleaned_data['ovenbird'])
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
    adser = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    class Meta:
        model = Ads
        fields = ['title', 'image', 'link', 'adser']
        
    def clean_adser(self):
        data = Adser.objects.get(id=self.cleaned_data['adser'])
        if not data:
            raise forms.ValidationError()
        return data
   
    def save(self, commit=True):
        object = super(AdsForm, self).save(commit=False)
        if commit:
            object.save()
        return object