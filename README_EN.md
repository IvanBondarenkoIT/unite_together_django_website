# Unite Together - Django Web Application

[![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-4169E1?logo=postgresql)](https://www.postgresql.org/)

## 📋 Overview

Unite Together is a web application for providing social assistance and support. The application allows registering and managing information about people in need, publishing news and projects, and coordinating assistance.

## ✨ Key Features

- 🧑‍💼 **User Profile Management** - Complete authentication and authorization system
- 👥 **Person Registration and Management** - Detailed database of people in need
- 📰 **News System** - News publishing with photo galleries and external links
- 🎯 **Projects** - Project management with categories and galleries
- 📝 **Dynamic Forms** - Forms with data validation and multilingual support
- 🔐 **Social Authentication** - Google OAuth2 integration
- 💳 **Payment Integration** - PayPal integration
- 🌍 **Multilingual Support** - Ukrainian and English languages
- 📱 **Responsive Design** - Mobile-first approach
- ☁️ **Cloud Deployment** - AWS/Azure support

## 🛠 Technology Stack

### Backend
- **Python 3.8+**
- **Django 5.0**
- **PostgreSQL** (main database for production)
- **SQLite** (for local development)
- **Django Allauth** (social authentication)
- **python-decouple** (environment variables management)

### Frontend
- **HTML5, CSS3, JavaScript**
- **Bootstrap 5**
- **jQuery**
- **Custom CSS** (mobile-first design)

### Infrastructure
- **AWS/Azure** (for production)
- **WhiteNoise** (static files serving)
- **Gunicorn** (WSGI server)

## 📦 System Requirements

- Python 3.8 or higher
- PostgreSQL 13+ (for production)
- pip (Python package manager)
- Git

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/IvanBondarenkoIT/unite_together_django_website.git
cd unite_together_django_website
```

### 2. Create Virtual Environment

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

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy `.env-sample` to `.env`:
   ```bash
   cp .env-sample .env
   ```

2. Edit `.env` and fill in required variables:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_ADMIN=your-email@example.com
   EMAIL_PASSWORD=your-email-password
   
   # PayPal settings
   PAYPAL_RECEIVER_EMAIL=your-paypal@example.com
   PAYPAL_ITEM_NAME=Donation
   PAYPAL_TEST=True
   PAYPAL_SUM=10
   
   # Database (for production)
   RDS_DB_NAME=your_db_name
   RDS_USERNAME=your_db_user
   RDS_PASSWORD=your_db_password
   RDS_HOSTNAME=your_db_host
   RDS_PORT=5432
   
   # Azure settings (if using)
   AZURE_RDS_PASSWORD=your_azure_password
   
   # Google OAuth2 (if using)
   SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-client-id
   SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-client-secret
   ```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/`

## 📁 Project Structure

```
unite_together_django_website/
├── about_us/              # "About Us" app
├── accounts/              # User management and authentication
├── coordination/          # Assistance coordination
├── donate/                # Donations and payments
├── homepage/              # Homepage
├── persons/               # Person management
├── web_pages/             # News, projects, events
├── templates/             # HTML templates
│   ├── aboutus/           # About Us templates
│   ├── accounts/          # Authentication templates
│   ├── news/             # News templates
│   ├── projects/         # Project templates
│   └── ...
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploaded files
├── staticfiles/           # Collected static files (not in git)
├── unite_together_django_website/  # Project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URLconf
│   └── wsgi.py           # WSGI configuration
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── .env-sample           # Environment variables example
└── README.md             # This file
```

## 🗄 Database Configuration

### Local Development (SQLite)

SQLite is used by default for local development. The `db.sqlite3` file is created automatically.

### Production (PostgreSQL)

Configure environment variables to connect to PostgreSQL:

```env
RDS_DB_NAME=your_database
RDS_USERNAME=your_username
RDS_PASSWORD=your_password
RDS_HOSTNAME=your_host
RDS_PORT=5432
```

Or for Azure:

```env
AZURE_RDS_PASSWORD=your_azure_password
```

## 🔒 Security

- ✅ All secrets stored in environment variables (`.env`)
- ✅ `.env` file added to `.gitignore`
- ✅ `SECRET_KEY` not stored in code
- ✅ Database passwords not stored in code
- ✅ API keys stored in environment variables

**⚠️ Important:** Never commit the `.env` file to Git!

## 📝 Common Commands

```bash
# Apply migrations
python manage.py migrate

# Create new migration
python manage.py makemigrations

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run tests
python manage.py test
```

## 🌐 Deployment

### AWS Elastic Beanstalk

1. Install AWS CLI and EB CLI
2. Run `eb init`
3. Configure environment variables in AWS console
4. Run `eb deploy`

### Azure

1. Set up Azure App Service
2. Add environment variables in Azure Portal
3. Configure PostgreSQL on Azure
4. Deploy via Git or Azure CLI

## 📚 Additional Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Allauth Documentation](https://docs.allauth.org/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to your branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the `LICENSE.txt` file for details.

## 📧 Contact

For additional information, contact: **ivan.bondarenko.it@gmail.com**

## 🙏 Acknowledgments

Thanks to everyone who participated in the development of this project.

---

**Version:** 1.0.0  
**Last Updated:** 2025

