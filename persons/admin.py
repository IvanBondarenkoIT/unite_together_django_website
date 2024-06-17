from django.contrib import admin
# from import_export.admin import ExportMixin
# from import_export.formats.base_formats import XLS

from django.utils.translation import gettext_lazy as _

from accounts.models import Account
from .models import AssociatedPerson, Participant, UserProfile, Person, TypeOfDocument


@admin.register(TypeOfDocument)
class TypeOfDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'regex')


# class PersonAdmin(admin.ModelAdmin):
#     list_display = (
#         'first_name', 'last_name', 'date_of_birth', 'citizenship', 'date_of_arrival',
#         'type_of_document', 'document_number', 'gender', 'georgian_phone_number',
#         'ukrainian_phone_number', 'country', 'chosen_city', 'address_line', 'created_at',
#         'updated_at', 'is_active', 'edit_permission', 'is_approved', 'user_owner'
#     )
#     list_filter = (
#         'gender', 'country', 'is_active', 'is_approved', 'citizenship', 'type_of_document',
#         'chosen_city', 'created_at', 'updated_at'
#     )
#     search_fields = ('first_name', 'last_name', 'document_number', 'georgian_phone_number', 'ukrainian_phone_number')
#     ordering = ('-created_at',)
#
#     fieldsets = (
#         (None, {
#             'fields': ('user_owner', 'first_name', 'last_name', 'date_of_birth', 'gender')
#         }),
#         ('Contact Info', {
#             'fields': ('georgian_phone_number', 'ukrainian_phone_number', 'address_line', 'chosen_city', 'country')
#         }),
#         ('Document Info', {
#             'fields': ('type_of_document', 'document_number', 'citizenship', 'date_of_arrival')
#         }),
#         ('Status', {
#             'fields': ('is_active', 'edit_permission', 'is_approved')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at')
#         }),
#     )


class UserOwnerFilter(admin.SimpleListFilter):
    title = _('User Owner')
    parameter_name = 'user_owner'

    def lookups(self, request, model_admin):
        users = Account.objects.all()
        return [(user.id, user.username) for user in users]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_owner_id=self.value())
        return queryset


class AssociatedPersonAdmin(admin.ModelAdmin):
    list_display = (
        'unique_identifier', 'user_owner', 'first_name', 'last_name', 'date_of_birth', 'citizenship', 'date_of_arrival',
        'type_of_document', 'document_number', 'gender', 'georgian_phone_number',
        'ukrainian_phone_number', 'country', 'chosen_city', 'address_line', 'created_at',
        'updated_at', 'is_active',
    )
    list_filter = (
        'unique_identifier', UserOwnerFilter, 'gender', 'country', 'is_active', 'is_approved', 'citizenship', 'type_of_document',
        'chosen_city', 'created_at', 'updated_at'
    )
    search_fields = ('unique_identifier', 'first_name', 'last_name', 'document_number', 'georgian_phone_number', 'ukrainian_phone_number')
    ordering = ('-created_at',)  # Default sorting by created_at descending
    # formats = [XLS]


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('copy_of_unique_identifier', 'registered_on','created_at', 'first_name', 'last_name', 'date_of_birth', 'date_of_birth', 'document_number', 'created_at', 'is_active')
    list_display_links = ('first_name', 'last_name')
    # readonly_fields = ('date_joined', 'last_login')
    ordering = ('-created_at',)

    filter_horizontal = ()
    list_filter = ('copy_of_unique_identifier', 'registered_on',)
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'person')


# admin.site.register(Person, PersonAdmin)
admin.site.register(AssociatedPerson, AssociatedPersonAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(UserProfile, UserProfileAdmin)