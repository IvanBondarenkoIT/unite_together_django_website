from django.contrib import admin
from web_pages.models import WebPage, WebPageSection, WebContentObject


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


admin.site.register(WebPage, WebPageAdmin)
admin.site.register(WebPageSection, WebPageSectionAdmin)
admin.site.register(WebContentObject, WebContentObjectAdmin)
