from django import forms
from django.forms import modelformset_factory

from .models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
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

PersonFormSet = modelformset_factory(Person, form=PersonForm, extra=0)
