# -*- coding: utf-8 -*-
from django import forms
from offsite.models import Ovenbird, City, Object

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
        widget=forms.TextInput
    )
    type = forms.IntegerField(
        widget=forms.HiddenInput
    )

    class Meta:
        model = Object
        fields = ['title', 'text', 'price', 'type']
        
    def __init__(self, *args, **kwargs):
        super(ObjectForm, self).__init__(*args, **kwargs)
        self.fields['type'].initial = kwargs.pop('type', None)
        
    def save(self, commit=True):
        object = super(ObjectForm, self).save(commit=False)
        if commit:
            object.save()
        return user