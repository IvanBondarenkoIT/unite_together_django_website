from django import forms
from web_pages.models import Events
from persons.models import Participant, AssociatedPerson


class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = '__all__'

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_arrival': forms.DateInput(attrs={'type': 'date'}),
            'type_of_document': forms.Select(attrs={'placeholder': 'Type of Document'}),
            'country': forms.Select(),
            'chosen_city': forms.Select(),
            'gender': forms.Select(),
        }


class AssociatedPersonForm(forms.ModelForm):
    class Meta:
        model = AssociatedPerson
        fields = '__all__'

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_arrival': forms.DateInput(attrs={'type': 'date'}),
            'type_of_document': forms.Select(attrs={'placeholder': 'Type of Document'}),
            'country': forms.Select(),
            'chosen_city': forms.Select(),
            'gender': forms.Select(),
        }
