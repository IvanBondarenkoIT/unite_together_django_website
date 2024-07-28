# forms.py
from django import forms
from .models import Projects, Events, ObjectsGroup


class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = '__all__'

        widgets = {
            'start_date': forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}),
            'end_date': forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = ObjectsGroup.objects.filter(page__name__iexact='projects')


class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = '__all__'

        widgets = {
            'start_date': forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}),
            'end_date': forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = ObjectsGroup.objects.filter(page__name__iexact='events')
