from django.contrib import admin
from web_pages.models import WebPage, WebContentObject, WebContentSubordinateObject, Events, ObjectsGroup, City


# Register your models here.

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_address')


class WebPageAdmin(admin.ModelAdmin):
    list_display = ('name',)


class WebContentObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'text', 'image', 'is_active', 'created_at', 'updated_at',)
    list_editable = ('is_active', )
    prepopulated_fields = {'slug': ('name',)}


class WebContentSubordinateObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'text',)


class ObjectsGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'text', 'image', 'is_active', 'created_at', 'updated_at',)
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name', 'group')}


admin.site.register(City, CityAdmin)
admin.site.register(WebPage, WebPageAdmin)
admin.site.register(WebContentObject, WebContentObjectAdmin)
admin.site.register(WebContentSubordinateObject, WebContentSubordinateObjectAdmin)
admin.site.register(ObjectsGroup, ObjectsGroupAdmin)
admin.site.register(Events, EventAdmin)
