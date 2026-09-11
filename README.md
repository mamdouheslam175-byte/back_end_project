# DevPulse — Django Blog Course Assignment

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

A clean, modern, and production-ready blog web application built strictly with **Function-Based Views (FBVs)**, **Django templates**, and **Vanilla CSS**. Built to fulfill and exceed all course assignment specifications.

---

## 🌟 Features & Assignment Specifications

### Part 1 — Core Setup
- Standard Django project structure (`myblog`) with root-level `manage.py`.
- Registered `blog` app inside `INSTALLED_APPS`.
- Zero-warning startup on `python manage.py runserver`.

### Part 2 — Models
- **Category Model**:
  - `name`: Unique, required string field.
  - `slug`: Auto-generated unique URL slug from name.
  - `__str__`: Returns category name.
  - Helper methods: `published_post_count`, `get_absolute_url`.
- **Post Model**:
  - `title`, `slug` (auto-generated), `content` (long text).
  - `category`: `ForeignKey` to `Category` with cascade deletion.
  - `author`: `ForeignKey` to Django built-in `User`.
  - `created_at` & `updated_at`: Auto-timestamped fields.
  - `is_published`: Boolean flag defaulting to `False` (draft).
  - `__str__`: Returns post title.
  - `Meta`: Ordered by `-created_at` (newest first).

### Part 3 — Django Admin
- Fully registered `Category` and `Post` in `admin.py`.
- **PostAdmin**:
  - `list_display`: Title, Category, Author, Published status, Created date, Reading time.
  - `list_filter`: Filterable by `category`, `is_published`, and `created_at`.
  - `search_fields`: Searchable by `title` and `content`.
  - `prepopulated_fields`: Slug auto-fills from title.
  - Bulk actions: Quickly publish or unpublish selected articles.
- Superuser setup instructions & automated seed script.

### Part 4 — Function-Based Views & Templates
- **Story 5 (Homepage)**: FBV (`post_list`) querying `is_published=True` ordered by newest first.
- **Story 6 (Detail Page)**: Route `/post/<slug>/` using `get_object_or_404`. Strict 404 guard for draft (`is_published=False`) or missing posts.
- **Story 7 (Category Filter)**: Route `/category/<slug>/` filtering published posts by category, cleanly reusing the `post_list.html` template.
- **Story 8 (Pagination)**: 5 posts per page using `Paginator`. Robust exception handling for `PageNotAnInteger` (serves page 1) and `EmptyPage` (serves last page).
- **Template System**: Clean template inheritance with `base.html` and reusable blocks.

### Part 5 — Bonus Features
- ⏱️ **Reading Time Estimate**: Computed dynamically using ~200 WPM reading pace (displayed on post cards and detail view).
- 🔍 **Search Engine using `Q` Objects**: Global search bar supporting simultaneous searches across article titles and content.
- ⚡ **Automated Data Seeding**: Custom management command `python manage.py seed_blog` to create categories, sample posts, and an admin user.
- 🎨 **Modern Design System**: Dark-slate aesthetic, glassmorphism header, responsive layout, smooth micro-animations.

---

## 📁 Project Directory Structure

```
.
├── manage.py                   # Django CLI entrypoint
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── myblog/                     # Project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py             # Settings, apps, templates, static
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py
├── blog/                       # Core Blog application
│   ├── __init__.py
│   ├── admin.py                # Admin portal configurations
│   ├── apps.py                 # App configuration
│   ├── context_processors.py   # Global template category provider
│   ├── models.py               # Category & Post models
│   ├── tests.py                # Automated unit tests
│   ├── urls.py                 # FBV URL routing
│   ├── utils.py                # Reading time estimator
│   ├── views.py                # Function-based views (FBVs)
│   ├── management/             # Custom management commands
│   │   └── commands/
│   │       └── seed_blog.py    # Seed command
│   └── migrations/             # Database migrations
├── templates/                  # Django HTML templates
│   ├── base.html               # Shared base template
│   └── blog/
│       ├── post_list.html      # Posts list, category filter & search
│       └── post_detail.html    # Full post detail view
└── static/                     # Static assets
    ├── css/
    │   └── style.css           # Vanilla CSS modern design system
    └── js/
        └── main.js             # Client-side UX enhancements
```

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** and **Git** installed on your system.

```bash
python --version
git --version
```

### 2. Clone the Repository
```bash
git clone https://github.com/<your-username>/django-blog-course-assignment.git
cd django-blog-course-assignment
```

### 3. Create & Activate Virtual Environment
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations
Apply the initial schema migrations for Django auth, content types, sessions, and the blog app:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser
You can create a superuser interactively:
```bash
python manage.py createsuperuser
```
*(Follow the prompts to enter username, email, and password).*

#### ✨ Instant Demo Setup (Recommended)
Alternatively, populate sample categories, published/draft posts, and create a ready-to-use superuser in one command:
```bash
python manage.py seed_blog
```
- **Demo Superuser**: `admin`
- **Demo Password**: `admin12345`

### 7. Run the Development Server
```bash
python manage.py runserver
```
Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser!

---

## 🧪 Running Automated Tests

A comprehensive unit test suite in `blog/tests.py` validates models, slug generation, reading time calculations, function-based views, 404 error handling, category filtering, search queries, and pagination:

```bash
python manage.py test blog
```

---

## 🔑 Available Routes

| Route | View Name | Description |
|---|---|---|
| `/` | `blog:post_list` | Homepage listing published posts (5 per page) |
| `/?q=keyword` | `blog:post_list` | Search results using Django `Q` objects |
| `/post/<slug>/` | `blog:post_detail` | Single post view (returns 404 for drafts) |
| `/category/<slug>/` | `blog:category_posts` | Filtered posts by category slug |
| `/admin/` | `admin:index` | Django Admin Portal |

---

## 📦 Git & GitHub Workflow

If setting up your remote GitHub repository for the first time:

```bash
# 1. Initialize git (if not already initialized)
git init

# 2. Stage all files
git add .

# 3. Create initial commit
git commit -m "feat: complete Django blog assignment with FBVs, models, and styling"

# 4. Add remote repository
git remote add origin https://github.com/<your-username>/django-blog-course-assignment.git

# 5. Push to main
git branch -M main
git push -u origin main
```
