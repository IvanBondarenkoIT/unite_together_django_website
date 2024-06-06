from django.contrib import admin
from .models import AssociatedPerson, Participant, UserProfile, Person


# class PersonAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'document_number', 'created_at', 'is_active')
#     list_display_links = ('first_name', 'last_name')
#     # readonly_fields = ('date_joined', 'last_login')
#     # ordering = ('-date_joined',)
#
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()


class AssociatedPersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'updated_at', 'created_at', 'is_active')
    list_display_links = ('first_name', 'last_name')
    # readonly_fields = ('date_joined', 'last_login')
    # ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('registered_on', 'first_name', 'last_name', 'date_of_birth', 'date_of_birth', 'document_number', 'created_at', 'is_active')
    list_display_links = ('first_name', 'last_name')
    # readonly_fields = ('date_joined', 'last_login')
    ordering = ('-created_at',)

    filter_horizontal = ()
    list_filter = ('registered_on',)
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'person')


# admin.site.register(Person, PersonAdmin)
admin.site.register(AssociatedPerson, AssociatedPersonAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(UserProfile, UserProfileAdmin)