import re
from django import forms

from unite_together_django_website.validators import CustomPasswordValidator
from .models import Account


class RegistrationForm(forms.ModelForm):
    agree_to_terms = forms.BooleanField(
        required=True, label="Я погоджуюсь з умовами використання"
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Введіть пароль",
                "class": "form-control",
            }
        ),
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Повторіть пароль",
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "phone_number", "email", "password"]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "Ім'я"
        self.fields["first_name"].widget.attrs["required"] = True
        self.fields["last_name"].widget.attrs["placeholder"] = "Прізвище"
        self.fields["last_name"].widget.attrs["required"] = True
        self.fields["phone_number"].widget.attrs["placeholder"] = "Номер телефону"
        self.fields["phone_number"].widget.attrs["required"] = True
        self.fields["email"].widget.attrs["placeholder"] = "Електрона адреса"
        self.fields["email"].widget.attrs["required"] = True
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Пароль не співпадає. Будласка спробуйте ще раз"
            )

        CustomPasswordValidator().validate(password)

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise forms.ValidationError("Ім'я є обов'язковим.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise forms.ValidationError("Прізвище є обов'язковим.")
        return last_name

    def clean_georgian_phone_number(self):
        georgian_phone_number = self.cleaned_data.get("georgian_phone_number")
        if georgian_phone_number:
            pattern = r"^995[0-9]{9}$"
            if not re.match(pattern, georgian_phone_number):
                raise forms.ValidationError(
                    "Грузинський номер телефону має бути у форматі: 995XXXXXXXXX."
                )
            return georgian_phone_number
        else:
            raise forms.ValidationError("Грузинський номер телефону є обов'язковим.")

    def clean_agree_to_terms(self):
        agree = self.cleaned_data.get("agree_to_terms")
        if not agree:
            raise forms.ValidationError("Ви повинні погодитися з умовами використання.")
        return agree
