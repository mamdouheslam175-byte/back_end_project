from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .utils import calculate_reading_time


class Category(models.Model):
    """
    Category model representing post categories/tags.
    Requirements:
    - name: unique, required, with auto-generated slug.
    - __str__ returns the category name.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique name for the category (required)."
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        help_text="URL-friendly slug. Auto-generated if left blank."
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Ensure unique slug even if names have special character differences
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})

    @property
    def published_post_count(self):
        return self.posts.filter(is_published=True).count()


class Post(models.Model):
    """
    Post model representing individual blog articles.
    Requirements:
    - title, slug, content (long text).
    - category (ForeignKey to Category).
    - author (ForeignKey to Django's built-in User).
    - created_at & updated_at (auto timestamps).
    - is_published (boolean, default False).
    - __str__ returns the post title.
    """
    title = models.CharField(
        max_length=200,
        help_text="Title of the blog post."
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True,
        help_text="URL slug for post identification. Auto-generated from title."
    )
    content = models.TextField(
        help_text="Main content body of the post."
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text="The category this post belongs to."
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        help_text="The author of this post."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the post was first created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the post was last modified."
    )
    is_published = models.BooleanField(
        default=False,
        help_text="Designates whether this post is published and visible publicly."
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    @property
    def reading_time(self):
        """Bonus feature: estimated reading time in minutes."""
        return calculate_reading_time(self.content)
