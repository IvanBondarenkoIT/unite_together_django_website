import re

from django import forms
from django.forms import modelformset_factory

from .models import AssociatedPerson, Participant, TypeOfDocument


class AssociatedPersonAdminForm(forms.ModelForm):

    class Meta:
        model = AssociatedPerson
        fields = '__all__'

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_arrival': forms.DateInput(attrs={'type': 'date'}),
        }


class AssociatedPersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssociatedPersonForm, self).__init__(*args, **kwargs)
        self.fields['document_number'].help_text = 'Select a document type to see the format.'

        if 'type_of_document' in self.data:
            try:
                type_of_document_id = self.data.get('type_of_document')
                type_of_document = TypeOfDocument.objects.get(id=type_of_document_id)
                self.fields['document_number'].help_text = type_of_document.hint if type_of_document else self.fields['document_number'].help_text
            except (ValueError, TypeOfDocument.DoesNotExist) as e:
                # Consider logging the error here
                pass
        elif self.instance.pk:
            self.fields['document_number'].help_text = self.instance.type_of_document.hint if self.instance.type_of_document else self.fields['document_number'].help_text

    class Meta:
        model = AssociatedPerson
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'citizenship', 'date_of_arrival',
            'type_of_document', 'document_number', 'gender', 'georgian_phone_number',
            'ukrainian_phone_number', 'country', 'chosen_city', 'address_line', 'is_active'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_arrival': forms.DateInput(attrs={'type': 'date'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'citizenship': forms.TextInput(attrs={'placeholder': 'Citizenship'}),
            'document_number': forms.TextInput(attrs={'placeholder': 'Document Number'}),
            'georgian_phone_number': forms.TextInput(attrs={'placeholder': 'Georgian Phone Number', 'pattern': '\\+995[0-9]{9}'}),
            'ukrainian_phone_number': forms.TextInput(attrs={'placeholder': 'Ukrainian Phone Number', 'pattern': '\\+380[0-9]{9}'}),
            'address_line': forms.TextInput(attrs={'placeholder': 'Address Line'}),
        }

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

    def clean_georgian_phone_number(self):
        georgian_phone_number = self.cleaned_data.get('georgian_phone_number')
        pattern = r'^\+995[0-9]{9}$'
        if georgian_phone_number and not re.match(pattern, georgian_phone_number):
            raise forms.ValidationError("Georgian phone number must be in the format: +995XXXXXXXXX.")
        return georgian_phone_number

    def clean_ukrainian_phone_number(self):
        ukrainian_phone_number = self.cleaned_data.get('ukrainian_phone_number')
        pattern = r'^\+380[0-9]{9}$'
        if ukrainian_phone_number and not re.match(pattern, ukrainian_phone_number):
            raise forms.ValidationError("Ukrainian phone number must be in the format: +380XXXXXXXXX.")
        return ukrainian_phone_number


class ParticipantAdminForm(forms.ModelForm):

    class Meta:
        model = Participant
        fields = '__all__'

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_arrival': forms.DateInput(attrs={'type': 'date'}),
        }

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
