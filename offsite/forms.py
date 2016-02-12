# -*- coding: utf-8 -*-
from django import forms
from offsite.models import Ovenbird, City, Object
import logging
logger = logging.getLogger(__name__)

class OvenbirdForm(forms.ModelForm):

    name = forms.CharField(
        label="Имя или название организации",
        widget=forms.TextInput
    )
    city_id = forms.ModelChoiceField(
        label="Город",
        queryset = City.objects.all(),
        required=False
    )
    telephone = forms.CharField(
        label="Телефон",
        widget=forms.TextInput
    )
    text = forms.CharField(
        label="Информация",
        widget=forms.Textarea
    )

    class Meta:
        model = Ovenbird
        fields = ['name', 'city', 'telephone', 'text']
        
    def __init__(self, *args, **kwargs):
        city = kwargs.pop('city', None)
        super(OvenbirdForm, self).__init__(*args, **kwargs)
        if city:
            self.fields['city'].queryset = City.objects.filter(id=city)
            
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
        widget=forms.Textarea
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