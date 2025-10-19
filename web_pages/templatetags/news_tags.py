from django import template

register = template.Library()

MONTH_TRANSLATIONS = {
    "Jan": {
        "uk": "Січ",
        "en": "Jan",
    },
    "Feb": {
        "uk": "Лют",
        "en": "Feb",
    },
    "Mar": {
        "uk": "Бер",
        "en": "Mar",
    },
    "Apr": {
        "uk": "Кві",
        "en": "Apr",
    },
    "May": {
        "uk": "Тра",
        "en": "May",
    },
    "Jun": {
        "uk": "Чер",
        "en": "Jun",
    },
    "Jul": {
        "uk": "Лип",
        "en": "Jul",
    },
    "Aug": {
        "uk": "Сер",
        "en": "Aug",
    },
    "Sep": {
        "uk": "Вер",
        "en": "Sep",
    },
    "Oct": {
        "uk": "Жов",
        "en": "Oct",
    },
    "Nov": {
        "uk": "Лис",
        "en": "Nov",
    },
    "Dec": {
        "uk": "Гру",
        "en": "Dec",
    },
}


@register.filter
def translate_month(month_abbr, lang="uk"):
    """
    Translates month abbreviation to specified language
    Usage: {{ news.get_start_date_month|translate_month:lang }}
    """
    return MONTH_TRANSLATIONS.get(month_abbr, {}).get(lang, month_abbr)

