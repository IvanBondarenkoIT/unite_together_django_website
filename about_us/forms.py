from django import forms


class ContactForm(forms.Form):
    FIRST_NAME_MAX_LENGTH = 50
    LAST_NAME_MAX_LENGTH = 50
    EMAIL_MAX_LENGTH = 254

    SUBJECT_CHOICES = [
        ("help", "Мені потрібна допомога"),
        ("volunteer", "Хочу допомогти"),
        ("job", "Подати заявку на роботу"),
        ("complaints", "Скарги та пропозиції"),
        ("partnership", "Партнерство та співпраця"),
    ]

    first_name = forms.CharField(
        max_length=FIRST_NAME_MAX_LENGTH, required=True, label="Ім'я"
    )
    last_name = forms.CharField(
        max_length=LAST_NAME_MAX_LENGTH, required=True, label="Прізвище"
    )
    email = forms.EmailField(
        max_length=EMAIL_MAX_LENGTH, required=True, label="Електронна пошта"
    )
    phone_number = forms.CharField(max_length=20, required=True, label="Номер телефону")
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, required=True, label="Тема")
    message = forms.CharField(
        widget=forms.Textarea, required=True, label="Повідомлення"
    )
