# -*- coding: utf-8 -*-
from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Filter, Location
from django.utils.html import format_html

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

admin.site.register(Location, LocationAdmin)
admin.site.register(Filter, FilternAdmin)