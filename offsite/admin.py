# -*- coding: utf-8 -*-
from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Filter, Location, Ovenbird
from django.utils.html import format_html

from django.conf.urls import patterns, url
from offsite.views import views, vkviews
from django.http import HttpResponse

class LocationAdmin(DraggableMPTTAdmin):
    tree_title_field = 'name'
    
class FilternAdmin(DraggableMPTTAdmin):
    tree_title_field = 'name'
    list_per_page = 2000
    list_display = ('tree_actions', 'indented_title','level')
    list_display_links = ('indented_title','level')
    mptt_level_indent = 20
    
    def level(self, instance):
        return format_html(
            '<div>{}</div>',
            instance._mpttfield('level'),
        )

class MyModelAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super(MyModelAdmin, self).get_urls()

        my_urls = [
             url(r'^admin_view/$', self.admin_site.admin_view(self.upload), name="myadmin"),
        ]

        return my_urls + urls
    
    def upload(self, request):
        return HttpResponse("dfdf")

admin.site.register(Location, LocationAdmin)
admin.site.register(Filter, FilternAdmin)