from django import forms
from django.forms import modelformset_factory

from .models import AssociatedPerson, Participant


class AssociatedPersonForm(forms.ModelForm):
    class Meta:
        model = AssociatedPerson
        fields = [
            'user_owner',
            'first_name',
            'last_name',
            'date_of_birth',
            'citizenship',
            'type_of_document',
            'date_of_arrival',
            'document_number',
            'gender',
            'georgian_phone_number',
            'ukrainian_phone_number',
            'country',
            'city',
            'region',
            'address_line',
        ]


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            'registered_on',
            'first_name',
            'last_name',
            'date_of_birth',
            'citizenship',
            'date_of_arrival',
            'type_of_document',
            'document_number',
            'gender',
            'georgian_phone_number',
            'ukrainian_phone_number',
            'country',
            'city',
            'region',
            'address_line',

        ]


ParticipantFormSet = modelformset_factory(Participant, form=ParticipantForm, extra=0)
AssociatedPersonFormSet = modelformset_factory(AssociatedPerson, form=AssociatedPersonForm, extra=0)
