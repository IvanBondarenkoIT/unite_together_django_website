# Unite Together - Django Web Application

[![Django](https://img.shields.io/badge/Django-3.2-092E20?logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-4169E1?logo=postgresql)](https://www.postgresql.org/)

## Огляд

Unite Together - це веб-додаток, розроблений для надання соціальної допомоги та підтримки. Додаток дозволяє реєструвати та керувати інформацією про осіб, які потребують допомоги, а також координувати надання цієї допомоги.

## Основні можливості

- 🧑‍💼 Управління профілями користувачів
- 👥 Реєстрація та ведення обліку осіб, які потребують допомоги
- 📝 Динамічні форми з валідацією даних
- 🔐 Аутентифікація через соціальні мережі
- 💳 Інтеграція з платіжними системами (PayPal)
- 🌍 Підтримка мультимовності (українська мова)
- ☁️ Розгортання на хмарних сервісах (AWS/Azure)

## Технологічний стек

### Бекенд
- **Python 3.8+**
- **Django 3.2**
- **PostgreSQL** (основна база даних)
- **SQLite** (для розробки)
- **Django REST Framework** (для API)
- **Django Allauth** (аутентифікація)

### Фронтенд
- HTML5, CSS3, JavaScript
- Bootstrap 5
- jQuery

### Інфраструктура
- AWS/Azure (для продакшн)
- Docker (для контейнеризації)
- Nginx (веб-сервер)
- Gunicorn (WSGI сервер)

## Вимоги до системи

- Python 3.8 або вище
- PostgreSQL 13+
- pip (менеджер пакетів Python)
- Node.js 14+ (для фронтенд залежностей)

## Встановлення та налаштування

1. **Клонування репозиторію**
   ```bash
   git clone <repository-url>
   cd unite_together_django_website
   ```

2. **Створення віртуального оточення та активація**
   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows: .\venv\Scripts\activate
   ```

3. **Встановлення залежностей**
   ```bash
   pip install -r requirements.txt
   ```

4. **Налаштування змінних оточення**
   - Скопіюйте `.env-sample` в `.env`
   - Заповніть необхідні змінні оточення

5. **Застосування міграцій**
   ```bash
   python manage.py migrate
   ```

6. **Створення суперкористувача**
   ```bash
   python manage.py createsuperuser
   ```

7. **Запуск сервера розробки**
   ```bash
   python manage.py runserver
   ```

## Налаштування бази даних

Додаток підтримує різні конфігурації баз даних:

### Розробка (SQLite)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Продакшн (PostgreSQL на AWS/Azure)
Налаштуйте відповідні змінні оточення у файлі `.env`.

## Розгортання

### AWS Elastic Beanstalk
1. Встановіть AWS CLI та EB CLI
2. Виконайте `eb init`
3. Виконайте `eb create`

### Docker
```bash
docker-compose up --build
```

## Ліцензія

Цей проект поширюється під ліцензією MIT. Детальніше див. у файлі `LICENSE.txt`.

## Контакти

Для отримання додаткової інформації звертайтеся за адресою ivan.bondarenko.it@gmail.com.

## Внесення змін

1. Зробіть форк репозиторію
2. Створіть гілку для вашої функції (`git checkout -b feature/amazing-feature`)
3. Зробіть коміт ваших змін (`git commit -m 'Add some amazing feature'`)
4. Відправте зміни у вашу гілку (`git push origin feature/amazing-feature`)
5. Відкрийте Pull Request

## Подяка

Дякуємо всім, хто брав участь у розробці цього проекту.