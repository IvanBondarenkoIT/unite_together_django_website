import re
from django import forms

from unite_together_django_website.validators import CustomPasswordValidator
from .models import Account


class RegistrationForm(forms.ModelForm):
    """
    Форма для регистрации новых пользователей. Включает поля для ввода имени, фамилии,
    номера телефона, электронной почты, пароля и подтверждения пароля, а также поле
    для согласия с условиями использования.
    """

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
        """
        Инициализация формы, которая добавляет классы Bootstrap и плейсхолдеры к полям,
        делая форму более удобной для пользователя.
        """
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
        """
        Проверка формы на соответствие условиям:
        - Пароли должны совпадать.
        - Пароль должен соответствовать требованиям CustomPasswordValidator.
        """
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Пароль не співпадає. Будь ласка спробуйте ще раз"
            )

        # Валидация пароля через кастомный валидатор
        CustomPasswordValidator().validate(password)

    def clean_first_name(self):
        """
        Проверка на корректность введенного имени:
        - Поле обязательно для заполнения.
        - Имя должно содержать только латинские буквы.
        """
        first_name = self.cleaned_data.get("first_name")

        if not first_name:
            raise forms.ValidationError("Ім'я є обов'язковим.")
        else:
            pattern = r"^[A-Za-z]+$"
            if not re.match(pattern, first_name):
                raise forms.ValidationError(
                    "Ім'я повинне складатися лише з латинських літер."
                )

        return first_name

    def clean_last_name(self):
        """
        Проверка на корректность введенной фамилии:
        - Поле обязательно для заполнения.
        - Фамилия должна содержать только латинские буквы.
        """
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise forms.ValidationError("Прізвище є обов'язковим.")
        else:
            pattern = r"^[A-Za-z]+$"
            if not re.match(pattern, last_name):
                raise forms.ValidationError(
                    "Прізвище повинне складатися лише з латинських літер."
                )

        return last_name

    def clean_georgian_phone_number(self):
        """
        Проверка грузинского номера телефона:
        - Поле обязательно для заполнения.
        - Номер должен быть в формате 995XXXXXXXXX.
        """
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

    def clean_email(self):
        """
        Проверка электронной почты:
        - Поле обязательно для заполнения.
        - Электронная почта должна соответствовать стандартному формату.
        """
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Електронна пошта є обов'язковим.")
        else:
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(pattern, email):
                raise forms.ValidationError("Некоректна електронна пошта.")

        return email

    def clean_agree_to_terms(self):
        """
        Проверка, согласен ли пользователь с условиями использования:
        - Поле обязательно для заполнения.
        """
        agree = self.cleaned_data.get("agree_to_terms")
        if not agree:
            raise forms.ValidationError("Ви повинні погодитися з умовами використання.")
        return agree
