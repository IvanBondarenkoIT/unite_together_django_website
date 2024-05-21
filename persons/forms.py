from django import forms
from .models import Person
from accounts.models import Account


# class RegistrationForm(forms.ModelForm):
    # Name
    # "Olga"
    # Surname
    # "Popova"
    # Gender
    # "Female"
    # Date of Birth
    # "12.02.1998"
    # Citizenship
    # "Ukrainian"
    # Type of document
    # "International Passport"
    # Date of arrival
    # "12.02.2024"
    # Document number
    # "FA803309"
    # Address
    # ""
    # Country
    # "Georgia"
    # City
    # "Batumi"
    # Region
    # "Ajaria"
    # Address Line
    # "35 Crescent Road"
    #
    # Email
    # "olga.popova@gmail.com"
    # Georgian Phone Number
    # "+995 595 720 458"
    # Ukrainian Phone Number
    # "+380 96 00 91 791"
    # password = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "placeholder": "Enter Password",
    #             "class": "form-control",
    #         }
    #     )
    # )
    #
    # confirm_password = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "placeholder": "Repeat Password",
    #             "class": "form-control",
    #         }
    #     )
    # )
    #
    # class Meta:
    #     model = Person
    #     fields = ["first_name", "last_name", "phone_number", "email", "password"]
    #
    # def __init__(self, *args, **kwargs):
    #     super(RegistrationForm, self).__init__(*args, **kwargs)
    #     self.fields["first_name"].widget.attrs["placeholder"] = "Enter First Name"
    #     self.fields["last_name"].widget.attrs["placeholder"] = "Enter Last Name"
    #     self.fields["phone_number"].widget.attrs["placeholder"] = "Enter Phone Number"
    #     self.fields["email"].widget.attrs["placeholder"] = "Enter Email Address"
    #     for field in self.fields:
    #         self.fields[field].widget.attrs["class"] = "form-control"
    #
    # def clean(self):
    #     cleaned_data = super(RegistrationForm, self).clean()
    #     password = cleaned_data.get("password")
    #     confirm_password = cleaned_data.get("confirm_password")
    #
    #     if password != confirm_password:
    #         raise forms.ValidationError(
    #             "Password is not matched. Please try again."
    #         )


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
