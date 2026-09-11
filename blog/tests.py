from django.contrib.admin.sites import site
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Category, Post
from .utils import calculate_reading_time


class BlogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='Django Framework')

    def test_category_creation_and_str(self):
        """Category __str__ should return category name, and slug should auto-generate."""
        self.assertEqual(str(self.category), 'Django Framework')
        self.assertEqual(self.category.slug, 'django-framework')

    def test_category_unique_slug_fallback(self):
        """Duplicate category names or slugs are safely handled."""
        cat2 = Category(name='Django Framework 2')
        cat2.save()
        self.assertEqual(cat2.slug, 'django-framework-2')

    def test_post_creation_and_str(self):
        """Post __str__ should return post title, and slug should auto-generate."""
        post = Post.objects.create(
            title='Learning Django Models',
            content='Django models define the data structure and business logic.',
            category=self.category,
            author=self.user,
            is_published=True
        )
        self.assertEqual(str(post), 'Learning Django Models')
        self.assertEqual(post.slug, 'learning-django-models')
        self.assertEqual(post.reading_time, 1)

    def test_reading_time_calculation(self):
        """Reading time should estimate 200 words per minute, min 1 min."""
        short_text = "This is a brief post."
        self.assertEqual(calculate_reading_time(short_text), 1)

        long_text = "word " * 450
        # 450 words / 200 wpm = 2.25 -> ceil = 3
        self.assertEqual(calculate_reading_time(long_text), 3)


class BlogViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='writer', password='password123')
        self.cat_python = Category.objects.create(name='Python')
        self.cat_frontend = Category.objects.create(name='Frontend')

        # Create 7 published posts in Python category
        self.published_posts = []
        for i in range(1, 8):
            p = Post.objects.create(
                title=f'Python Post {i}',
                content=f'Comprehensive content body for Python post number {i}.',
                category=self.cat_python,
                author=self.user,
                is_published=True
            )
            self.published_posts.append(p)

        # Create 1 unpublished draft in Python category
        self.draft_post = Post.objects.create(
            title='Secret Python Draft',
            content='This post is not published yet and should not be publicly accessible.',
            category=self.cat_python,
            author=self.user,
            is_published=False
        )

        # Create 1 published post in Frontend category
        self.frontend_post = Post.objects.create(
            title='Modern CSS Tricks',
            content='Flexbox and CSS Grid allow clean layouts.',
            category=self.cat_frontend,
            author=self.user,
            is_published=True
        )

    def test_homepage_shows_published_posts_only(self):
        """Story 5: Homepage returns 200, shows published posts, excludes drafts."""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)

        # Published posts should be in context
        page_posts = response.context['posts']
        for post in page_posts:
            self.assertTrue(post.is_published)

        # Draft post should NOT appear anywhere in the page HTML
        self.assertNotContains(response, 'Secret Python Draft')

    def test_homepage_pagination(self):
        """Story 8: Homepage paginates with 5 posts per page."""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 5)
        self.assertTrue(response.context['page_obj'].has_next())

    def test_pagination_page_not_an_integer(self):
        """Story 8: Non-integer page query gracefully falls back to page 1."""
        response = self.client.get(reverse('blog:post_list') + '?page=notanumber')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].number, 1)

    def test_pagination_empty_page_out_of_range(self):
        """Story 8: Out of range page query gracefully falls back to last page."""
        response = self.client.get(reverse('blog:post_list') + '?page=99999')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['page_obj'].number,
            response.context['paginator'].num_pages
        )

    def test_post_detail_published(self):
        """Story 6: Detail page loads for published post."""
        post = self.published_posts[0]
        url = reverse('blog:post_detail', kwargs={'slug': post.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.content)

    def test_post_detail_unpublished_returns_404(self):
        """Story 6: Detail page returns 404 if is_published=False."""
        url = reverse('blog:post_detail', kwargs={'slug': self.draft_post.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_detail_nonexistent_returns_404(self):
        """Story 6: Detail page returns 404 for invalid slug."""
        url = reverse('blog:post_detail', kwargs={'slug': 'non-existent-slug-xyz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_category_filter(self):
        """Story 7: Category filter returns published posts in that category only."""
        url = reverse('blog:category_posts', kwargs={'slug': self.cat_frontend.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Modern CSS Tricks')
        self.assertNotContains(response, 'Python Post 1')

    def test_category_filter_nonexistent_returns_404(self):
        """Story 7: Nonexistent category slug returns 404."""
        url = reverse('blog:category_posts', kwargs={'slug': 'missing-cat-404'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_search_with_q_objects(self):
        """Bonus Feature: Search query filters posts matching title or content."""
        response = self.client.get(reverse('blog:post_list') + '?q=Tricks')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Modern CSS Tricks')
        self.assertNotContains(response, 'Python Post 1')


class BlogAdminRegistrationTests(TestCase):
    def test_admin_models_registered(self):
        """Part 3: Post and Category are registered in Django Admin."""
        self.assertIn(Category, site._registry)
        self.assertIn(Post, site._registry)
