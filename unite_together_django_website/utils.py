from django.core.mail import send_mail

from django.core.mail import send_mail


send_mail(
    "Тестовое письмо",
    "Привет! Это тестовое письмо для проверки настройки SMTP.",
    "info@unite-together.org",  # Отправитель
    ["krenkroyt@gmail.com"],  # Получатель
    fail_silently=False,
)
