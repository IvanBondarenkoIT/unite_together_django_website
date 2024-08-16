from django import forms

from unite_together_django_website.validators import CustomPasswordValidator
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Введіть пароль",
                "class": "form-control",
            }
        )
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
        self.fields["last_name"].widget.attrs["placeholder"] = "Прізвище"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Номер телефону"
        self.fields["email"].widget.attrs["placeholder"] = "Електрона адреса"
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

