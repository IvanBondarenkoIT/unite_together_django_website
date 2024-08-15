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


    # def __init__(self, *args, **kwargs):
    #     super(AssociatedPersonForm, self).__init__(*args, **kwargs)
    #     self.fields['document_number'].help_text = 'Select a document type to see the format.'
    #
    #     if 'type_of_document' in self.data:
    #         try:
    #             type_of_document_id = self.data.get('type_of_document')
    #             type_of_document = TypeOfDocument.objects.get(id=type_of_document_id)
    #             self.fields['document_number'].help_text = type_of_document.hint if type_of_document else self.fields['document_number'].help_text
    #         except (ValueError, TypeOfDocument.DoesNotExist) as e:
    #             # Consider logging the error here
    #             pass
    #     elif self.instance.pk:
    #         self.fields['document_number'].help_text = self.instance.type_of_document.hint if self.instance.type_of_document else self.fields['document_number'].help_text


class AssociatedPersonForm(forms.ModelForm):

    class Meta:
        model = AssociatedPerson
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'citizenship', 'date_of_arrival',
            'type_of_document', 'document_number', 'gender', 'georgian_phone_number',
            'ukrainian_phone_number', 'country', 'chosen_city', 'address_line', 'is_active'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'date_of_arrival': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'required': True}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'required': True}),
            'citizenship': forms.Select(attrs={
                'placeholder': 'Citizenship',
                'class': 'form-control',
                'required': True,
            }),
            'type_of_document': forms.Select(attrs={
                'placeholder': 'Type of Document',
                'class': 'form-control',
                'required': True,
            }),
            'document_number': forms.TextInput(attrs={'placeholder': 'Document Number', 'required': True}),
            'georgian_phone_number': forms.TextInput(attrs={
                'placeholder': 'Georgian Phone Number',
                'pattern': r'^\995[0-9]{9}$',
                'required': True,
            }),
            'ukrainian_phone_number': forms.TextInput(attrs={'placeholder': 'Ukrainian Phone Number', 'pattern': r'^\380[0-9]{9}$'}),
            'address_line': forms.TextInput(attrs={'placeholder': 'Address Line', 'required': True}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     user_owner = kwargs.get('user_owner')
    #     if user_owner and hasattr(user_owner, 'associated_person'):
    #         self.fields['georgian_phone_number'].initial = user_owner.associated_person.georgian_phone_number

    def clean_document_number(self):
        type_of_document = self.cleaned_data.get('type_of_document')
        if type_of_document:
            document_number = self.cleaned_data.get('document_number')
            pattern = type_of_document.regex
            if document_number and not re.match(pattern, document_number):
                raise forms.ValidationError(f"Document Type: {type_of_document.name} must be formatted as {type_of_document.hint}")
            return document_number
        else:
            raise forms.ValidationError("Document Type must be chosen")

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
        if georgian_phone_number:
            pattern = r'^995[0-9]{9}$'
            if not re.match(pattern, georgian_phone_number):
                raise forms.ValidationError("Georgian phone number must be in the format: 995XXXXXXXXX.")
            return georgian_phone_number
        else:
            raise forms.ValidationError("Georgian phone number is required.")

    def clean_ukrainian_phone_number(self):
        ukrainian_phone_number = self.cleaned_data.get('ukrainian_phone_number')
        if ukrainian_phone_number:
            pattern = r'^380[0-9]{9}$'
            if not re.match(pattern, ukrainian_phone_number):
                raise forms.ValidationError("Ukrainian phone number must be in the format: 380XXXXXXXXX.")
            return ukrainian_phone_number
        return ukrainian_phone_number  # No validation error if the field is left empty


class ParticipantAdminForm(forms.ModelForm):

    class Meta:
        model = Participant
        fields = '__all__'

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_arrival': forms.DateInput(attrs={'type': 'date'}),
        }

AssociatedPersonFormSet = modelformset_factory(AssociatedPerson, form=AssociatedPersonForm, extra=0)
