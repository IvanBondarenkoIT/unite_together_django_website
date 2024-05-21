from django.contrib import admin
from .models import Person


# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'updated_at', 'created_at', 'is_active')
    list_display_links = ('first_name', 'last_name')
    # readonly_fields = ('date_joined', 'last_login')
    # ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Person, PersonAdmin)