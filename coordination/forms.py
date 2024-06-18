from django import forms
from web_pages.models import Events
from persons.models import Participant, Person


class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = '__all__'


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
