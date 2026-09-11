from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from blog.models import Category, Post


class Command(BaseCommand):
    help = "Populate the database with sample categories, posts, and a superuser."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding blog data..."))

        # 1. Create superuser
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            }
        )
        if created:
            admin_user.set_password("admin12345")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("[OK] Created superuser 'admin' with password 'admin12345'"))
        else:
            self.stdout.write(self.style.WARNING("[!] Superuser 'admin' already exists"))

        # Create a second author for variety
        author_jane, _ = User.objects.get_or_create(
            username="jane_dev",
            defaults={"email": "jane@example.com", "first_name": "Jane", "last_name": "Doe"}
        )

        # 2. Create Categories
        categories_data = [
            "Python & Django",
            "Web Development",
            "Database & APIs",
            "Architecture & Design",
            "DevOps & Tools",
        ]

        categories = {}
        for cat_name in categories_data:
            cat, _ = Category.objects.get_or_create(
                name=cat_name,
                defaults={"slug": slugify(cat_name)}
            )
            categories[cat_name] = cat
            self.stdout.write(self.style.SUCCESS(f"[OK] Category: {cat.name}"))

        # 3. Create Sample Posts
        posts_data = [
            {
                "title": "Mastering Django Function-Based Views",
                "category": "Python & Django",
                "author": admin_user,
                "is_published": True,
                "content": (
                    "Function-Based Views (FBVs) in Django offer unparalleled simplicity and clarity. "
                    "Unlike Class-Based Views which rely on multiple inheritance and method overrides, "
                    "FBVs allow you to follow the exact HTTP request-response lifecycle step by step.\n\n"
                    "In this article, we explore how explicit querying, pagination using Paginator, "
                    "and clean error handling with get_object_or_404 make your Django application "
                    "maintainable and easy to reason about for both beginners and experienced engineers."
                ),
            },
            {
                "title": "Understanding Django ORM and Q Objects for Advanced Search",
                "category": "Database & APIs",
                "author": admin_user,
                "is_published": True,
                "content": (
                    "When building search functionality in Django, basic filter lookups often fall short "
                    "if you need to query multiple fields simultaneously. This is where Q objects shine.\n\n"
                    "By using Q objects, you can construct complex SQL OR queries such as matching keywords "
                    "in both the article title and content body seamlessly without raw SQL."
                ),
            },
            {
                "title": "Clean Architecture in Django Applications",
                "category": "Architecture & Design",
                "author": author_jane,
                "is_published": True,
                "content": (
                    "Structuring a Django project for long-term scalability requires strict separation of concerns. "
                    "Keep your business logic decoupled from HTTP presentation layers, utilize domain services, "
                    "and keep models fat and views thin.\n\n"
                    "We will examine practical refactoring patterns, query optimization with select_related, "
                    "and best practices for reusable Django templates."
                ),
            },
            {
                "title": "Deploying Django with Gunicorn and Nginx",
                "category": "DevOps & Tools",
                "author": admin_user,
                "is_published": True,
                "content": (
                    "Taking a Django application from local development to production involves configuring WSGI "
                    "application servers, managing static assets with collectstatic, setting up reverse proxies, "
                    "and hardening environment variables.\n\n"
                    "Follow this comprehensive checklist to ensure zero-downtime deployments and optimal SSL caching."
                ),
            },
            {
                "title": "Modern Frontend Techniques with Vanilla CSS and Django Templates",
                "category": "Web Development",
                "author": author_jane,
                "is_published": True,
                "content": (
                    "You don't always need heavy JavaScript single-page application frameworks to build modern, "
                    "fast, and responsive web user experiences. Modern CSS features such as CSS Variables, "
                    "Flexbox, CSS Grid, and subtle backdrop filters enable stunning aesthetics with zero bundle overhead.\n\n"
                    "Learn how to structure shared base templates, template inheritance, and reusable component blocks."
                ),
            },
            {
                "title": "Building RESTful APIs with Django: Best Practices",
                "category": "Database & APIs",
                "author": admin_user,
                "is_published": True,
                "content": (
                    "RESTful architectural constraints provide consistency and predictability across client-server interactions. "
                    "Discover how proper HTTP status codes, pagination headers, and validation serializers "
                    "streamline frontend integrations."
                ),
            },
            {
                "title": "Draft: Upcoming Python 3.13 Features & Free-Threading",
                "category": "Python & Django",
                "author": admin_user,
                "is_published": False,  # Draft post (unpublished)
                "content": (
                    "This is an internal unpublished draft previewing Python 3.13 free-threading and JIT compilation experiments. "
                    "Because is_published=False, this article must NOT appear on the public homepage or category feeds, "
                    "and accessing its URL directly must return an HTTP 404 response."
                ),
            },
            {
                "title": "Draft: Secret Upcoming Architecture Overhaul",
                "category": "Architecture & Design",
                "author": author_jane,
                "is_published": False,  # Draft post (unpublished)
                "content": (
                    "Another unpublished draft for testing edge cases and 404 guards. "
                    "Non-published articles remain visible exclusively inside Django Admin for staff members."
                ),
            },
        ]

        for p_data in posts_data:
            cat = categories[p_data["category"]]
            post, created = Post.objects.get_or_create(
                title=p_data["title"],
                defaults={
                    "slug": slugify(p_data["title"]),
                    "content": p_data["content"],
                    "category": cat,
                    "author": p_data["author"],
                    "is_published": p_data["is_published"],
                }
            )
            status_str = "Published" if post.is_published else "Draft (Unpublished)"
            self.stdout.write(self.style.SUCCESS(f"[OK] Post: '{post.title}' [{status_str}]"))

        self.stdout.write(self.style.SUCCESS("\nDatabase seeding completed successfully!"))
        self.stdout.write(self.style.NOTICE("Superuser credentials: username='admin', password='admin12345'"))
