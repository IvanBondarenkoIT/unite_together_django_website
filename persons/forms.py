import re

from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from .models import AssociatedPerson, Participant


class AssociatedPersonAdminForm(forms.ModelForm):
    class Meta:
        model = AssociatedPerson
        fields = '__all__'
        # widgets = {
        #     'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        #     'date_of_arrival': forms.DateInput(attrs={'type': 'date'}),
        # }


class AssociatedPersonForm(forms.ModelForm):
    class Meta:
        model = AssociatedPerson
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'citizenship', 'date_of_arrival',
            'type_of_document', 'document_number', 'gender', 'georgian_phone_number',
            'ukrainian_phone_number', 'country', 'chosen_city', 'address_line', 'is_active'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'ДД.ММ.РРРР'}),
            'date_of_arrival': forms.DateInput(attrs={'type': 'date', 'placeholder': 'ДД.ММ.РРРР'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Ім\'я', 'required': True}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Прізвище', 'required': True}),
            'citizenship': forms.Select(attrs={
                'placeholder': 'Громадянство',
                'class': 'form-control',
                'required': True,
            }),
            'type_of_document': forms.Select(attrs={
                'placeholder': 'Тип документа',
                'class': 'form-control',
                'required': True,
            }),
            'document_number': forms.TextInput(attrs={'placeholder': 'Номер документа', 'required': True}),
            'georgian_phone_number': forms.TextInput(attrs={
                'placeholder': 'Грузинський номер телефону',
                'pattern': r'^\995[0-9]{9}$',
                'required': True,
            }),
            'ukrainian_phone_number': forms.TextInput(attrs={
                'placeholder': 'Український номер телефону',
                'pattern': r'^\380[0-9]{9}$'
            }),
            'address_line': forms.TextInput(attrs={'placeholder': 'Адреса', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        default_ge_phone = kwargs.pop('default_ge_phone', None)
        super().__init__(*args, **kwargs)
        if default_ge_phone:
            self.fields['georgian_phone_number'].initial = default_ge_phone

        # Перетворення формату дати для відображення у формі
        if self.instance.pk:  # Якщо об'єкт вже існує
            if self.instance.date_of_birth:
                self.fields['date_of_birth'].initial = self.instance.date_of_birth.strftime('%d.%m.%Y')
            if self.instance.date_of_arrival:
                self.fields['date_of_arrival'].initial = self.instance.date_of_arrival.strftime('%d.%m.%Y')

    def clean_document_number(self):
        type_of_document = self.cleaned_data.get('type_of_document')
        if type_of_document:
            document_number = self.cleaned_data.get('document_number')
            pattern = type_of_document.regex
            if document_number and not re.match(pattern, document_number):
                raise forms.ValidationError(
                    f"Тип документа: {type_of_document.name} повинен бути у форматі {type_of_document.hint}"
                )
            return document_number
        else:
            raise forms.ValidationError("Необхідно вибрати тип документа")

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("Ім'я є обов'язковим.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError("Прізвище є обов'язковим.")
        return last_name

    def clean_georgian_phone_number(self):
        georgian_phone_number = self.cleaned_data.get('georgian_phone_number')
        if georgian_phone_number:
            pattern = r'^995[0-9]{9}$'
            if not re.match(pattern, georgian_phone_number):
                raise forms.ValidationError("Грузинський номер телефону має бути у форматі: 995XXXXXXXXX.")
            return georgian_phone_number
        else:
            raise forms.ValidationError("Грузинський номер телефону є обов'язковим.")

    def clean_ukrainian_phone_number(self):
        ukrainian_phone_number = self.cleaned_data.get('ukrainian_phone_number')
        if ukrainian_phone_number:
            pattern = r'^380[0-9]{9}$'
            if not re.match(pattern, ukrainian_phone_number):
                raise forms.ValidationError("Український номер телефону має бути у форматі: 380XXXXXXXXX.")
            return ukrainian_phone_number
        return ukrainian_phone_number  # Відсутня помилка перевірки, якщо поле залишено порожнім

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if not date_of_birth:
            raise ValidationError("Дата народження є обов'язковою і повинна бути у форматі ДД.ММ.РРРР.")
        return date_of_birth

    def clean_date_of_arrival(self):
        date_of_arrival = self.cleaned_data.get('date_of_arrival')
        if not date_of_arrival:
            raise ValidationError("Дата прибуття є обов'язковою і повинна бути у форматі ДД.ММ.РРРР.")
        return date_of_arrival


class ParticipantAdminForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_arrival': forms.DateInput(attrs={'type': 'date'}),
        }


AssociatedPersonFormSet = modelformset_factory(AssociatedPerson, form=AssociatedPersonForm, extra=0)
