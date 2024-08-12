import datetime

import openpyxl
from django.contrib import admin
from django.http import HttpResponse
# from import_export.admin import ExportMixin
# from import_export.formats.base_formats import XLS

from django.utils.translation import gettext_lazy as _

from accounts.models import Account
from .forms import AssociatedPersonForm, AssociatedPersonAdminForm, ParticipantAdminForm
from .models import AssociatedPerson, Participant, UserProfile, Person, TypeOfDocument


@admin.register(TypeOfDocument)
class TypeOfDocumentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'hint', 'regex')



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
def export_associated_persons(modeladmin, request, queryset):
    # Create a workbook and add a worksheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'AssociatedPersons'

    # Write the headers
    headers = [
        'Unique ID',
        'First Name',
        'Last Name',
        'Date of Birth',
        'Citizenship',
        'Date of Arrival',
        'Type of Document',
        'Document Number',
        'Gender',
        'Georgian Phone Number',
        'Ukrainian Phone Number',
        'Country',
        'City',
        'Address Line',
        'Created At',
        'Updated At',
        'Is Active',
        'Edit Permission',
        'Is Approved',
        'User Owner Email'
    ]  # Adjust headers as needed
    sheet.append(headers)

    # Write data rows
    for person in queryset:
        sheet.append([
            person.unique_identifier,
            person.first_name,
            person.last_name,
            person.date_of_birth,
            person.citizenship,
            person.date_of_arrival,
            person.type_of_document.name if person.type_of_document else '',  # Assuming TypeOfDocument has a 'name' field
            person.document_number,
            person.gender,
            person.georgian_phone_number,
            person.ukrainian_phone_number,
            person.country,
            person.chosen_city.name if person.chosen_city else '',  # Assuming City has a 'name' field
            person.address_line,
            person.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            person.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            person.is_active,
            person.edit_permission,
            person.is_approved,
            person.user_owner.email if person.user_owner else ''
        ])  # Adjust fields as needed

    current_datetime = datetime.datetime.now()
    date_string = current_datetime.strftime("%d-%m-%Y")
    # Save the workbook to an HttpResponse
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="associated_persons_{date_string}.xlsx"'
    workbook.save(response)

    return response


export_associated_persons.short_description = "Export selected AssociatedPersons to Excel"

def export_participants(modeladmin, request, queryset):
    # Create a workbook and add a worksheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Participants'

    # Write the headers
    headers = [
        'Unique ID',
        'First Name',
        'Last Name',
        'Date of Birth',
        'Citizenship',
        'Date of Arrival',
        'Type of Document',
        'Document Number',
        'Gender',
        'Georgian Phone Number',
        'Ukrainian Phone Number',
        'Country',
        'City',
        'Address Line',
        'Created At',
        'Updated At',
        'Is Active',
        'Edit Permission',
        'Is Approved',
        'User Owner Email',
        'Copy of Unique Identifier',
        'Registered On (Event)',
        'Status'
    ]
    sheet.append(headers)

    # Write data rows
    for participant in queryset:
        sheet.append([
            participant.copy_of_unique_identifier,
            participant.first_name,
            participant.last_name,
            participant.date_of_birth,
            participant.citizenship,
            participant.date_of_arrival,
            participant.type_of_document.name if participant.type_of_document else '',  # Assuming TypeOfDocument has a 'name' field
            participant.document_number,
            participant.gender,
            participant.georgian_phone_number,
            participant.ukrainian_phone_number,
            participant.country,
            participant.chosen_city.name if participant.chosen_city else '',  # Assuming City has a 'name' field
            participant.address_line,
            participant.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            participant.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            participant.is_active,
            participant.edit_permission,
            participant.is_approved,
            participant.user_owner.email if participant.user_owner else '',
            participant.copy_of_unique_identifier,
            participant.registered_on.name if participant.registered_on else '',  # Assuming Events has a 'name' field
            participant.status
        ])

    current_datetime = datetime.datetime.now()
    date_string = current_datetime.strftime("%d-%m-%Y")
    # Save the workbook to an HttpResponse
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="participants_{date_string}.xlsx"'
    workbook.save(response)

    return response

export_participants.short_description = "Export selected Participants to Excel"


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
    form = AssociatedPersonAdminForm
    list_display = (
        'unique_identifier', 'user_owner', 'first_name', 'last_name', 'date_of_birth', 'citizenship', 'date_of_arrival',
        'type_of_document', 'document_number', 'gender', 'georgian_phone_number',
        'ukrainian_phone_number', 'country', 'chosen_city', 'address_line', 'created_at',
        'updated_at', 'is_active',
    )
    list_display_links = ('unique_identifier',)
    list_filter = (
        'unique_identifier', UserOwnerFilter, 'gender', 'country', 'is_active', 'is_approved', 'citizenship', 'type_of_document',
        'chosen_city', 'created_at', 'updated_at'
    )
    search_fields = ('unique_identifier', 'first_name', 'last_name', 'document_number', 'georgian_phone_number', 'ukrainian_phone_number')
    ordering = ('-created_at',)  # Default sorting by created_at descending
    # formats = [XLS]
    actions = [export_associated_persons]


class ParticipantAdmin(admin.ModelAdmin):
    form = ParticipantAdminForm
    list_display = ('copy_of_unique_identifier', 'registered_on', 'registered_date', 'first_name', 'last_name', 'date_of_birth', 'date_of_arrival', 'document_number', 'created_at', 'is_active')

    def registered_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')

    registered_date.short_description = 'Registered Date'

    list_display_links = ('copy_of_unique_identifier', 'first_name', 'last_name')
    # readonly_fields = ('date_joined', 'last_login')
    ordering = ('-created_at',)
    search_fields = ('copy_of_unique_identifier', 'first_name', 'last_name', 'document_number', 'georgian_phone_number',
                     'ukrainian_phone_number')
    filter_horizontal = ()
    list_filter = ('copy_of_unique_identifier', 'registered_on',)
    fieldsets = ()
    actions = [export_participants]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'person')


# admin.site.register(Person, PersonAdmin)
admin.site.register(AssociatedPerson, AssociatedPersonAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(UserProfile, UserProfileAdmin)