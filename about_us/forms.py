from django import forms


class ContactForm(forms.Form):
    FIRST_NAME_MAX_LENGTH = 50
    LAST_NAME_MAX_LENGTH = 50
    EMAIL_MAX_LENGTH = 254

    SUBJECT_CHOICES = [
        ('help', 'I need help'),
        ('volunteer', 'I want to help'),
        ('job', 'Apply for job'),
        ('complaints', 'Complaints and suggestions'),
        ('partnership', 'Partnership and collaboration'),
    ]

    first_name = forms.CharField(max_length=FIRST_NAME_MAX_LENGTH, required=True)
    last_name = forms.CharField(max_length=LAST_NAME_MAX_LENGTH, required=True)
    email = forms.EmailField(max_length=EMAIL_MAX_LENGTH, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
