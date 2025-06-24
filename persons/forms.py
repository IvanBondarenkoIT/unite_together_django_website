import re
from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from .models import AssociatedPerson, Participant


TRANSLATIONS = {
    "uk": {
        "first_name_required": "Ім'я є обов'язковим.",
        "first_name_invalid": "Ім'я повинне складатися лише з латинських літер.",
        "last_name_required": "Прізвище є обов'язковим.",
        "last_name_invalid": "Прізвище повинне складатися лише з латинських літер.",
        "dob_required": "Дата народження є обов'язковою.",
        "dob_underage": "У головної особи Вік повинен бути не менше 18 років.",
        "ge_phone_required": "Грузинський номер телефону є обов'язковим.",
        "ge_phone_invalid": "Грузинський номер телефону має бути у форматі: 995XXXXXXXXX.",
        "ua_phone_invalid": "Український номер телефону має бути у форматі: 380XXXXXXXXX.",
        "arrival_required": "Дата прибуття є обов'язковою і повинна бути у форматі ДД.ММ.РРРР.",
        "doc_type_required": "Необхідно вибрати тип документа.",
        "doc_invalid": "Тип документа: {name} повинен бути у форматі {hint}.",
    },
    "en": {
        "first_name_required": "First name is required.",
        "first_name_invalid": "First name must contain only Latin letters.",
        "last_name_required": "Last name is required.",
        "last_name_invalid": "Last name must contain only Latin letters.",
        "dob_required": "Date of birth is required.",
        "dob_underage": "Main person must be at least 18 years old.",
        "ge_phone_required": "Georgian phone number is required.",
        "ge_phone_invalid": "Georgian phone must be in the format: 995XXXXXXXXX.",
        "ua_phone_invalid": "Ukrainian phone must be in the format: 380XXXXXXXXX.",
        "arrival_required": "Date of arrival is required and must be in DD.MM.YYYY format.",
        "doc_type_required": "Document type must be selected.",
        "doc_invalid": "Document type: {name} must follow the format {hint}.",
    },
}


class AssociatedPersonAdminForm(forms.ModelForm):
    class Meta:
        model = AssociatedPerson
        fields = "__all__"


class AssociatedPersonForm(forms.ModelForm):
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
        }

    def __init__(self, *args, lang="uk", **kwargs):
        self.lang = lang
        self.translations = TRANSLATIONS.get(lang, TRANSLATIONS["uk"])
        self.user = kwargs.pop("user", None)
        default_ge_phone = kwargs.pop("default_ge_phone", None)
        super().__init__(*args, **kwargs)

        if default_ge_phone:
            self.fields["georgian_phone_number"].initial = default_ge_phone

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise ValidationError(self.translations["first_name_required"])
        if not re.match(r"^[A-Za-z]+$", first_name):
            raise ValidationError(self.translations["first_name_invalid"])
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise ValidationError(self.translations["last_name_required"])
        if not re.match(r"^[A-Za-z]+$", last_name):
            raise ValidationError(self.translations["last_name_invalid"])
        return last_name

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth")
        if not date_of_birth:
            raise ValidationError(self.translations["dob_required"])
        if self.instance and self.user and self.user.associated_person == self.instance:
            today = date.today()
            age = (
                today.year
                - date_of_birth.year
                - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            )
            if age < 18:
                raise ValidationError(self.translations["dob_underage"])
        return date_of_birth

    def clean_georgian_phone_number(self):
        ge_phone = self.cleaned_data.get("georgian_phone_number")
        if not ge_phone:
            raise ValidationError(self.translations["ge_phone_required"])
        if not re.match(r"^995[0-9]{9}$", ge_phone):
            raise ValidationError(self.translations["ge_phone_invalid"])
        return ge_phone

    # def clean_ukrainian_phone_number(self):
    #     ua_phone = self.cleaned_data.get("ukrainian_phone_number")
    #     if ua_phone and not re.match(r"^380[0-9]{9}$", ua_phone):
    #         raise ValidationError(self.translations["ua_phone_invalid"])
    #     return ua_phone
    #
    # def clean_date_of_arrival(self):
    #     date_of_arrival = self.cleaned_data.get("date_of_arrival")
    #     if not date_of_arrival:
    #         raise ValidationError(self.translations["arrival_required"])
    #     return date_of_arrival
    #
    # def clean_document_number(self):
    #     doc_type = self.cleaned_data.get("type_of_document")
    #     doc_number = self.cleaned_data.get("document_number")
    #     if not doc_type:
    #         raise ValidationError(self.translations["doc_type_required"])
    #     if doc_number and not re.match(doc_type.regex, doc_number):
    #         raise ValidationError(
    #             self.translations["doc_invalid"].format(
    #                 name=doc_type.name, hint=doc_type.hint
    #             )
    #         )
    #     return doc_number


class ParticipantAdminForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = "__all__"
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "date_of_arrival": forms.DateInput(attrs={"type": "date"}),
        }


AssociatedPersonFormSet = modelformset_factory(
    AssociatedPerson, form=AssociatedPersonForm, extra=0
)
