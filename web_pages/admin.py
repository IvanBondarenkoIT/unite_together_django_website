from django.contrib import admin
from web_pages.models import WebPage, WebPageSection, WebContentObject, WebContentSubordinateObject


# Register your models here.
class WebPageAdmin(admin.ModelAdmin):
    list_display = ('name',)


class WebPageSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'page', 'content',)
    # list_editable = ('is_active', )
    # list_filter = ('product', 'variation_category', 'variation_value')


class WebContentObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'text', 'image', 'is_active', 'created_at', 'updated_at',)
    list_editable = ('is_active', )
    # prepopulated_fields = {'slug': ('product_name',)}


class WebContentSubordinateObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'text', 'image', 'is_active', 'content_master_object',)
    list_editable = ('is_active', )


admin.site.register(WebPage, WebPageAdmin)
admin.site.register(WebPageSection, WebPageSectionAdmin)
admin.site.register(WebContentObject, WebContentObjectAdmin)
admin.site.register(WebContentSubordinateObject, WebContentSubordinateObjectAdmin)
