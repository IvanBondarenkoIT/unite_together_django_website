# Unite Together Project Structure

## 📂 General Structure

```
unite_together_django_website/
├── about_us/              # "About Us" app
├── accounts/              # User management
├── coordination/          # Assistance coordination
├── donate/                # Donation system
├── homepage/              # Homepage
├── persons/               # Person management
├── web_pages/             # News, projects, events
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS)
├── media/                 # Uploaded files
├── staticfiles/           # Collected static files
└── unite_together_django_website/  # Project settings
```

## 📦 Django Apps

### `about_us/`
**Purpose:** Organization information

**Main Models:**
- `Program` - organization programs
- `Document` - documents
- `Partners` - partners
- `Contacts` - contact information

**Main Views:**
- `about_us()` - main "About Us" page
- `documents()` - documents
- `partners()` - partners
- `contacts()` - contacts

### `accounts/`
**Purpose:** Authentication and user management

**Main Models:**
- `Account` - extended user model

**Features:**
- Django Allauth integration
- Social authentication (Google OAuth2)
- Custom pipeline for social login processing

### `web_pages/`
**Purpose:** Site content - news, projects, events

**Main Models:**
- `News` - news with photo galleries and external links
- `Projects` - projects with categories
- `Events` - events
- `NewsGallery` - photo gallery for news
- `ProjectGallery` - photo gallery for projects

**Main Views:**
- `news()` - news list
- `news_detail()` - news details
- `projects()` - projects list
- `projects_detail()` - project details

**Template Tags:**
- `news_tags.py` - tags for month translation

### `persons/`
**Purpose:** Management of people in need

**Main Models:**
- `Person` - main person model
- `DocumentType` - document types
- `City` - cities

**Features:**
- Complex forms with validation
- Multilingual support
- Data export (Excel)

### `homepage/`
**Purpose:** Site homepage

**Main Models:**
- `Section` - homepage sections
- `CallToAction` - call-to-action elements

**Features:**
- News carousel
- Content sections
- Responsive design

### `donate/`
**Purpose:** Donation system via PayPal

**Features:**
- PayPal IPN integration
- Payment processing
- Success/error pages

## 🎨 Frontend Structure

### `templates/`
Templates organized by apps and types:

```
templates/
├── base.html              # Base template
├── aboutus/               # "About Us" templates
│   ├── aboutus-index.html
│   ├── about-us-documents.html
│   └── ...
├── news/                  # News templates
│   ├── desktop/           # Desktop versions
│   └── mobile/            # Mobile versions
├── projects/              # Project templates
├── accounts/              # Authentication templates
├── persons/               # Person management templates
└── includes/              # Partial templates
    ├── new/
    │   ├── navbar.html    # Navigation menu
    │   └── ...
    └── ...
```

### `static/`
Static files organized by type:

```
static/
├── css/
│   ├── news/              # News styles
│   ├── projects/          # Project styles
│   ├── accounts/          # Account styles
│   └── ...
├── js/                    # JavaScript files
└── img/                   # Images
```

**Important:** Files from `static/` are automatically collected to `staticfiles/` by the `collectstatic` command.

## 🔧 Configuration

### `unite_together_django_website/settings.py`
Main Django settings file:

- **Database:** SQLite (dev) and PostgreSQL (prod) support
- **Static Files:** WhiteNoise for production
- **Media Files:** Local storage or Azure Blob Storage
- **Authentication:** Django Allauth with Google OAuth2
- **Languages:** Ukrainian (uk) and English (en)

### Environment Variables (`.env`)
All secrets and configuration stored in `.env`:

- `SECRET_KEY` - Django secret key
- `DEBUG` - debug mode
- `RDS_*` - PostgreSQL settings
- `EMAIL_*` - email settings
- `PAYPAL_*` - PayPal settings
- `SOCIAL_AUTH_*` - OAuth2 settings

## 📊 Database

### Main Tables:
- `auth_user` - Django users
- `accounts_account` - extended user data
- `web_pages_news` - news
- `web_pages_projects` - projects
- `persons_person` - persons
- `about_us_program` - programs

### Migrations:
All migrations are in `*/migrations/`. Latest migrations:
- `0037_news_url_link` - added url_link field for news

## 🚀 Deployment

### Local Development:
1. Uses SQLite
2. `DEBUG=True`
3. Static files from `static/`

### Production:
1. PostgreSQL on AWS/Azure
2. `DEBUG=False`
3. Static files from `staticfiles/` via WhiteNoise
4. Media files on Azure Blob Storage (optional)

## 📝 Best Practices

1. **Security:**
   - All secrets in `.env`
   - `.env` in `.gitignore`
   - Using `python-decouple`

2. **Code:**
   - Commented code removed
   - Clean code without dead code

3. **Structure:**
   - Logical organization by apps
   - Separation of desktop/mobile templates
   - Modular CSS files

4. **Versioning:**
   - Git for version control
   - Meaningful commits
   - `local-development` branch for development

## 🔍 Useful Commands

```bash
# Create migration
python manage.py makemigrations <app_name>

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

**Last Updated:** 2025

