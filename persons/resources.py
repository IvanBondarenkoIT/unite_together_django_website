from import_export import resources
from .models import AssociatedPerson


class AssociatedPersonResource(resources.ModelResource):
    class Meta:
        model = AssociatedPerson
        fields = (
            'id', 'first_name', 'last_name', 'gender', 'country', 'user_owner__username',
            'date_of_birth', 'citizenship', 'date_of_arrival', 'type_of_document__name',
            'document_number', 'georgian_phone_number', 'ukrainian_phone_number', 'address_line',
            'created_at', 'updated_at', 'is_active', 'edit_permission', 'is_approved'
        )
        export_order = fields

