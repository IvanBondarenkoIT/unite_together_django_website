# forms.py
from django import forms
from .models import Projects, Events, ObjectsGroup


class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = ObjectsGroup.objects.filter(page__name__iexact='projects')


class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = ObjectsGroup.objects.filter(page__name__iexact='events')
