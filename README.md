# Unite Together - Django Web Application

[![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-4169E1?logo=postgresql)](https://www.postgresql.org/)

## 📋 Огляд

Unite Together - це веб-додаток для надання соціальної допомоги та підтримки. Додаток дозволяє реєструвати та керувати інформацією про осіб, які потребують допомоги, публікувати новини та проєкти, координувати надання допомоги.

## ✨ Основні можливості

- 🧑‍💼 **Управління профілями користувачів** - повна система аутентифікації та авторизації
- 👥 **Реєстрація та ведення обліку осіб** - детальна база даних про людей, які потребують допомоги
- 📰 **Система новин** - публікація новин з фото-галереями та зовнішніми посиланнями
- 🎯 **Проєкти** - управління проєктами з категоріями та галереями
- 📝 **Динамічні форми** - форми з валідацією даних та мультимовною підтримкою
- 🔐 **Аутентифікація через соціальні мережі** - Google OAuth2
- 💳 **Інтеграція з платіжними системами** - PayPal
- 🌍 **Підтримка мультимовності** - українська та англійська мови
- 📱 **Адаптивний дизайн** - mobile-first підхід
- ☁️ **Розгортання на хмарних сервісах** - AWS/Azure

## 🛠 Технологічний стек

### Бекенд
- **Python 3.8+**
- **Django 5.0**
- **PostgreSQL** (основна база даних для продакшн)
- **SQLite** (для локальної розробки)
- **Django Allauth** (соціальна аутентифікація)
- **python-decouple** (управління змінними оточення)

### Фронтенд
- **HTML5, CSS3, JavaScript**
- **Bootstrap 5**
- **jQuery**
- **Custom CSS** (mobile-first дизайн)

### Інфраструктура
- **AWS/Azure** (для продакшн)
- **WhiteNoise** (обслуговування статичних файлів)
- **Gunicorn** (WSGI сервер)

## 📦 Вимоги до системи

- Python 3.8 або вище
- PostgreSQL 13+ (для продакшн)
- pip (менеджер пакетів Python)
- Git

## 🚀 Швидкий старт

### 1. Клонування репозиторію

```bash
git clone https://github.com/IvanBondarenkoIT/unite_together_django_website.git
cd unite_together_django_website
```

### 2. Створення віртуального оточення

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Встановлення залежностей

```bash
pip install -r requirements.txt
```

### 4. Налаштування змінних оточення

1. Скопіюйте файл `.env-sample` в `.env`:
   ```bash
   cp .env-sample .env
   ```

2. Відредагуйте `.env` та заповніть необхідні змінні:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_ADMIN=your-email@example.com
   EMAIL_PASSWORD=your-email-password
   
   # PayPal налаштування
   PAYPAL_RECEIVER_EMAIL=your-paypal@example.com
   PAYPAL_ITEM_NAME=Donation
   PAYPAL_TEST=True
   PAYPAL_SUM=10
   
   # База даних (для продакшн)
   RDS_DB_NAME=your_db_name
   RDS_USERNAME=your_db_user
   RDS_PASSWORD=your_db_password
   RDS_HOSTNAME=your_db_host
   RDS_PORT=5432
   
   # Azure налаштування (якщо використовуєте)
   AZURE_RDS_PASSWORD=your_azure_password
   
   # Google OAuth2 (якщо використовуєте)
   SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-client-id
   SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-client-secret
   ```

### 5. Застосування міграцій

```bash
python manage.py migrate
```

### 6. Збір статичних файлів

```bash
python manage.py collectstatic --noinput
```

### 7. Створення суперкористувача

```bash
python manage.py createsuperuser
```

### 8. Запуск сервера розробки

```bash
python manage.py runserver
```

Відкрийте браузер та перейдіть на `http://127.0.0.1:8000/`

## 📁 Структура проекту

```
unite_together_django_website/
├── about_us/              # Додаток "Про нас"
├── accounts/              # Управління користувачами та аутентифікація
├── coordination/          # Координація допомоги
├── donate/                # Пожертви та донати
├── homepage/              # Головна сторінка
├── persons/               # Управління особами
├── web_pages/             # Новости, проєкти, події
├── templates/             # HTML шаблони
│   ├── aboutus/           # Шаблони "Про нас"
│   ├── accounts/          # Шаблони аутентифікації
│   ├── news/             # Шаблони новин
│   ├── projects/         # Шаблони проєктів
│   └── ...
├── static/                # Статичні файли (CSS, JS, зображення)
├── media/                 # Завантажені файли користувачів
├── staticfiles/           # Зібрані статичні файли (не в git)
├── unite_together_django_website/  # Налаштування проекту
│   ├── settings.py       # Налаштування Django
│   ├── urls.py           # Головний URLconf
│   └── wsgi.py           # WSGI конфігурація
├── manage.py             # Django management script
├── requirements.txt      # Python залежності
├── .env-sample           # Приклад файлу змінних оточення
└── README.md             # Цей файл
```

## 🗄 Налаштування бази даних

### Локальна розробка (SQLite)

SQLite використовується за замовчуванням для локальної розробки. Файл `db.sqlite3` створюється автоматично.

### Продакшн (PostgreSQL)

Налаштуйте змінні оточення для підключення до PostgreSQL:

```env
RDS_DB_NAME=your_database
RDS_USERNAME=your_username
RDS_PASSWORD=your_password
RDS_HOSTNAME=your_host
RDS_PORT=5432
```

Або для Azure:

```env
AZURE_RDS_PASSWORD=your_azure_password
```

## 🔒 Безпека

- ✅ Всі секрети зберігаються в змінних оточення (`.env`)
- ✅ Файл `.env` додано в `.gitignore`
- ✅ `SECRET_KEY` не зберігається в коді
- ✅ Паролі баз даних не зберігаються в коді
- ✅ API ключі зберігаються в змінних оточення

**⚠️ Важливо:** Ніколи не комітьте файл `.env` в Git!

## 📝 Основні команди

```bash
# Застосувати міграції
python manage.py migrate

# Створити нову міграцію
python manage.py makemigrations

# Зібрати статичні файли
python manage.py collectstatic

# Створити суперкористувача
python manage.py createsuperuser

# Запустити сервер розробки
python manage.py runserver

# Запустити тести
python manage.py test
```

## 🌐 Розгортання

### AWS Elastic Beanstalk

1. Встановіть AWS CLI та EB CLI
2. Виконайте `eb init`
3. Налаштуйте змінні оточення в AWS консолі
4. Виконайте `eb deploy`

### Azure

1. Налаштуйте Azure App Service
2. Додайте змінні оточення в Azure Portal
3. Налаштуйте PostgreSQL на Azure
4. Деплойте через Git або Azure CLI

## 📚 Додаткова документація

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Allauth Documentation](https://docs.allauth.org/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)

## 🤝 Внесення змін

1. Зробіть форк репозиторію
2. Створіть гілку для вашої функції (`git checkout -b feature/amazing-feature`)
3. Зробіть коміт ваших змін (`git commit -m 'Add some amazing feature'`)
4. Відправте зміни у вашу гілку (`git push origin feature/amazing-feature`)
5. Відкрийте Pull Request

## 📄 Ліцензія

Цей проект поширюється під ліцензією MIT. Детальніше див. у файлі `LICENSE.txt`.

## 📧 Контакти

Для отримання додаткової інформації звертайтеся за адресою: **ivan.bondarenko.it@gmail.com**

## 🙏 Подяка

Дякуємо всім, хто брав участь у розробці цього проекту.

---

**Версія:** 1.0.0  
**Останнє оновлення:** 2025
