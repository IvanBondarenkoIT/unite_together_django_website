from django.contrib import admin
from web_pages.models import WebPage, WebContentObject, WebContentSubordinateObject, Events, ObjectsGroup


# Register your models here.
class WebPageAdmin(admin.ModelAdmin):
    list_display = ('name',)


class WebContentObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'text', 'image', 'is_active', 'created_at', 'updated_at',)
    list_editable = ('is_active', )
    prepopulated_fields = {'slug': ('name', 'group')}


class WebContentSubordinateObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'text',)


class ObjectsGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'text', 'image', 'is_active', 'created_at', 'updated_at',)
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name', 'group')}


admin.site.register(WebPage, WebPageAdmin)
admin.site.register(WebContentObject, WebContentObjectAdmin)
admin.site.register(WebContentSubordinateObject, WebContentSubordinateObjectAdmin)
admin.site.register(ObjectsGroup, ObjectsGroupAdmin)
admin.site.register(Events, EventAdmin)
