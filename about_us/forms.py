from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    FIRST_NAME_MAX_LENGTH = 50
    LAST_NAME_MAX_LENGTH = 50
    EMAIL_MAX_LENGTH = 254

    TRANSLATIONS = {
        "uk": {
            "first_name": "Ім'я",
            "last_name": "Прізвище",
            "email": "Електронна пошта",
            "phone_number": "Номер телефону",
            "subject": "Тема",
            "message": "Повідомлення",
            "subject_choices": [
                ("help", "Мені потрібна допомога"),
                ("volunteer", "Хочу допомогти"),
                ("job", "Подати заявку на роботу"),
                ("complaints", "Скарги та пропозиції"),
                ("partnership", "Партнерство та співпраця"),
            ],
        },
        "en": {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
            "phone_number": "Phone Number",
            "subject": "Subject",
            "message": "Message",
            "subject_choices": [
                ("help", "I need help"),
                ("volunteer", "I want to volunteer"),
                ("job", "Apply for a job"),
                ("complaints", "Complaints and suggestions"),
                ("partnership", "Partnership and cooperation"),
            ],
        },
    }

    def __init__(self, *args, lang="uk", **kwargs):
        print(f"form created {lang}")
        super().__init__(*args, **kwargs)
        self.lang = lang
        translation = self.TRANSLATIONS.get(lang, self.TRANSLATIONS["uk"])

        self.fields["first_name"].label = translation["first_name"]
        self.fields["last_name"].label = translation["last_name"]
        self.fields["email"].label = translation["email"]
        self.fields["phone_number"].label = translation["phone_number"]
        self.fields["subject"].label = translation["subject"]
        self.fields["subject"].choices = translation["subject_choices"]
        self.fields["message"].label = translation["message"]

    first_name = forms.CharField(max_length=FIRST_NAME_MAX_LENGTH, required=True)
    last_name = forms.CharField(max_length=LAST_NAME_MAX_LENGTH, required=True)
    email = forms.EmailField(max_length=EMAIL_MAX_LENGTH, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    subject = forms.ChoiceField(choices=[])
    message = forms.CharField(widget=forms.Textarea, required=True)
