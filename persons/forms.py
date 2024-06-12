from django import forms
from django.forms import modelformset_factory

from .models import AssociatedPerson, Participant, TypeOfDocument


# class AssociatedPersonForm(forms.ModelForm):
#     class Meta:
#         model = AssociatedPerson
#         fields = [
#             'user_owner',
#             'first_name',
#             'last_name',
#             'date_of_birth',
#             'citizenship',
#             'type_of_document',
#             'date_of_arrival',
#             'document_number',
#             'gender',
#             'georgian_phone_number',
#             'ukrainian_phone_number',
#             'country',
#             'city',
#             'region',
#             'address_line',
#         ]


class AssociatedPersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssociatedPersonForm, self).__init__(*args, **kwargs)
        self.fields['document_number'].help_text = 'Select a document type to see the format.'

        if 'type_of_document' in self.data:
            try:
                type_of_document_id = self.data.get('type_of_document')
                type_of_document = TypeOfDocument.objects.get(id=type_of_document_id)
                self.fields['document_number'].help_text = type_of_document.hint
            except (ValueError, TypeOfDocument.DoesNotExist):
                pass
        elif self.instance.pk:
            self.fields['document_number'].help_text = self.instance.type_of_document.hint

    class Meta:
        model = AssociatedPerson
        fields = [
            'first_name', 'last_name', 'date_of_birth',
            'citizenship', 'date_of_arrival', 'type_of_document', 'document_number',
            'gender', 'georgian_phone_number', 'ukrainian_phone_number',
            'country', 'chosen_city', 'address_line', 'is_active'
        ]

        # 'country', 'type_of_document', 'chosen_city',
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_arrival': forms.DateInput(attrs={'type': 'date'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'citizenship': forms.TextInput(attrs={'placeholder': 'Citizenship'}),
            'type_of_document': forms.Select(attrs={'placeholder': 'Type of Document'}),
            'document_number': forms.TextInput(attrs={'placeholder': 'Document Number'}),
            'georgian_phone_number': forms.TextInput(attrs={'placeholder': 'Georgian Phone Number'}),
            'ukrainian_phone_number': forms.TextInput(attrs={'placeholder': 'Ukrainian Phone Number'}),
            'country': forms.Select(),
            'chosen_city': forms.Select(),
            'address_line': forms.TextInput(attrs={'placeholder': 'Address Line'}),
            'gender': forms.Select(),
        }

    # def clean_document_number(self):
    #     document_number = self.cleaned_data.get('document_number')
    #
    #     if document_number and document_number < 0:
    #         raise forms.ValidationError("Document number cannot be negative.")
    #     return document_number

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("First name is required.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError("Last name is required.")
        return last_name

    # Add any additional custom validation here




#
# class ParticipantForm(forms.ModelForm):
#     class Meta:
#         model = Participant
#         fields = [
#             'registered_on',
#             'first_name',
#             'last_name',
#             'date_of_birth',
#             'citizenship',
#             'date_of_arrival',
#             'type_of_document',
#             'document_number',
#             'gender',
#             'georgian_phone_number',
#             'ukrainian_phone_number',
#             'country',
#             'city',
#             'region',
#             'address_line',
#
#         ]


# ParticipantFormSet = modelformset_factory(Participant, form=ParticipantForm, extra=0)
AssociatedPersonFormSet = modelformset_factory(AssociatedPerson, form=AssociatedPersonForm, extra=0)
