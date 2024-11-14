import re
from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from .models import AssociatedPerson, Participant
from datetime import date


class AssociatedPersonAdminForm(forms.ModelForm):
    """
    Form used in the Django admin for managing AssociatedPerson instances.
    """

    class Meta:
        model = AssociatedPerson
        fields = "__all__"
        list_filter = ("user_owner",)  # Filters by 'user_owner' in admin
        search_fields = ["first_name", "last_name", "user_owner__unique_identifier"]

        def get_associated_person(self, obj):
            """
            Returns the associated person related to the user_owner.
            """
            return obj.user_owner.associated_person

        get_associated_person.short_description = "Associated Person"


class AssociatedPersonForm(forms.ModelForm):
    """
    Form for collecting detailed information about an associated person.
    Includes validation for fields like first name, last name, date of birth,
    and phone numbers.
    """

    class Meta:
        model = AssociatedPerson
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "citizenship",
            "date_of_arrival",
            "type_of_document",
            "document_number",
            "gender",
            "georgian_phone_number",
            "ukrainian_phone_number",
            "country",
            "chosen_city",
            "address_line",
            "is_active",
            "criteria",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "date_of_arrival": forms.DateInput(attrs={"type": "date"}),
            "first_name": forms.TextInput(
                attrs={"placeholder": "Ім'я(Латиницею)", "required": True}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Прізвище(Латиницею)", "required": True}
            ),
            "citizenship": forms.Select(
                attrs={
                    "placeholder": "Громадянство",
                    "class": "form-control",
                    "required": True,
                }
            ),
            "type_of_document": forms.Select(
                attrs={
                    "placeholder": "Тип документа",
                    "class": "form-control",
                    "required": True,
                }
            ),
            "document_number": forms.TextInput(
                attrs={"placeholder": "Номер документа", "required": True}
            ),
            "georgian_phone_number": forms.TextInput(
                attrs={
                    "placeholder": "Грузинський номер телефону",
                    "pattern": r"^\995[0-9]{9}$",
                    "required": True,
                }
            ),
            "ukrainian_phone_number": forms.TextInput(
                attrs={
                    "placeholder": "Український номер телефону",
                    "pattern": r"^\380[0-9]{9}$",
                }
            ),
            "address_line": forms.TextInput(
                attrs={"placeholder": "Адреса", "required": True}
            ),
            "criteria": forms.Select(
                attrs={
                    "placeholder": "Крітерій вразливості",
                    "class": "form-control",
                    "required": True,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Custom initializer to set default values for fields like Georgian phone number.
        """
        self.user = kwargs.pop("user", None)
        default_ge_phone = kwargs.pop("default_ge_phone", None)
        super().__init__(*args, **kwargs)
        if default_ge_phone:
            self.fields["georgian_phone_number"].initial = default_ge_phone

    def clean_date_of_birth(self):
        """
        Validates that the date of birth is provided and that the user is at least 18 years old.
        """
        date_of_birth = self.cleaned_data.get("date_of_birth")
        if not date_of_birth:
            raise ValidationError("Дата народження є обов'язковою.")

        if self.instance and self.user and self.user.associated_person == self.instance:
            today = date.today()
            age = (
                today.year
                - date_of_birth.year
                - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            )
            if age < 18:
                raise ValidationError(
                    "У головної особи Вік повинен бути не менше 18 років."
                )
        return date_of_birth

    def clean_document_number(self):
        """
        Ensures the document number matches the pattern for the specified document type.
        """
        type_of_document = self.cleaned_data.get("type_of_document")
        if type_of_document:
            document_number = self.cleaned_data.get("document_number")
            pattern = type_of_document.regex
            if document_number and not re.match(pattern, document_number):
                raise forms.ValidationError(
                    f"Тип документа: {type_of_document.name} повинен бути у форматі {type_of_document.hint}"
                )
            return document_number
        else:
            raise forms.ValidationError("Необхідно вибрати тип документа")

    def clean_first_name(self):
        """
        Validates that the first name is in Latin characters and is provided.
        """
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise forms.ValidationError("Ім'я є обов'язковим.")
        if not re.match(r"^[A-Za-z]+$", first_name):
            raise forms.ValidationError(
                "Ім'я повинне складатися лише з латинських літер."
            )
        return first_name

    def clean_last_name(self):
        """
        Validates that the last name is in Latin characters and is provided.
        """
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise forms.ValidationError("Прізвище є обов'язковим.")
        if not re.match(r"^[A-Za-z]+$", last_name):
            raise forms.ValidationError(
                "Прізвище повинне складатися лише з латинських літер."
            )
        return last_name

    def clean_georgian_phone_number(self):
        """
        Checks that the Georgian phone number is in the correct format.
        """
        georgian_phone_number = self.cleaned_data.get("georgian_phone_number")
        if georgian_phone_number:
            if not re.match(r"^995[0-9]{9}$", georgian_phone_number):
                raise forms.ValidationError(
                    "Грузинський номер телефону має бути у форматі: 995XXXXXXXXX."
                )
            return georgian_phone_number
        else:
            raise forms.ValidationError("Грузинський номер телефону є обов'язковим.")

    def clean_ukrainian_phone_number(self):
        """
        Validates that the Ukrainian phone number is correctly formatted, if provided.
        """
        ukrainian_phone_number = self.cleaned_data.get("ukrainian_phone_number")
        if ukrainian_phone_number:
            if not re.match(r"^380[0-9]{9}$", ukrainian_phone_number):
                raise forms.ValidationError(
                    "Український номер телефону має бути у форматі: 380XXXXXXXXX."
                )
        return ukrainian_phone_number

    def clean_date_of_arrival(self):
        """
        Validates that the date of arrival is provided.
        """
        date_of_arrival = self.cleaned_data.get("date_of_arrival")
        if not date_of_arrival:
            raise ValidationError(
                "Дата прибуття є обов'язковою і повинна бути у форматі ДД.ММ.РРРР."
            )
        return date_of_arrival


class ParticipantAdminForm(forms.ModelForm):
    """
    Form for managing Participant instances within the admin interface.
    """

    class Meta:
        model = Participant
        fields = "__all__"
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "date_of_arrival": forms.DateInput(attrs={"type": "date"}),
        }


# Formset for managing multiple associated persons
AssociatedPersonFormSet = modelformset_factory(
    AssociatedPerson, form=AssociatedPersonForm, extra=0
)
