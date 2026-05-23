# yourapp/templatetags/trans_lang.py
from django import template

register = template.Library()

TRANSLATIONS = {
    "last_event": {
        "uk": "Останній відвіданий захід:",
        "en": "Last visited event:",
    },
    "go_to_registration": {
        "uk": "Перейти до реєстрації",
        "en": "Go to registration",
    },
    "main_person": {
        "uk": "Головна Особа:",
        "en": "Main Person:",
    },
    "family_tree": {
        "uk": "Родина",
        "en": "Family Tree",
    },
    "georgian_phone": {
        "uk": "Грузинський номер телефону:",
        "en": "Georgian phone number:",
    },
    "ukrainian_phone": {
        "uk": "Український номер телефону:",
        "en": "Ukrainian phone number:",
    },
    "address": {
        "uk": "Адреса:",
        "en": "Address:",
    },
    "full_info": {
        "uk": "Повна інформація",
        "en": "Full info",
    },
    "edit_request": {
        "uk": "Щоб редагувати особу, відправте запит",
        "en": "To edit the person, send a request",
    },
    "add_person": {
        "uk": "Додати нову особу",
        "en": "Add new person",
    },
    "actions": {
        "uk": "Дії",
        "en": "Actions",
    },
    "name": {
        "uk": "Ім'я",
        "en": "Name",
    },
    "birthdate": {
        "uk": "Дата народження",
        "en": "Date of birth",
    },
    "document_number": {
        "uk": "Номер документу",
        "en": "Document number",
    },
    "gender": {
        "uk": "Стать",
        "en": "Gender",
    },
    "edit": {
        "uk": "Редагувати",
        "en": "Edit",
    },
}


@register.simple_tag
def trans_lang(key, lang="uk"):
    return TRANSLATIONS.get(key, {}).get(lang, key)
