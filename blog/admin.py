from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.
    """
    list_display = ('name', 'slug', 'get_total_posts')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description="Total Posts")
    def get_total_posts(self, obj):
        return obj.posts.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for Post model.
    Requirements:
    - Register Post and Category in admin.py.
    - Configure list_display, list_filter (by category, is_published), and search_fields (by title).
    """
    list_display = (
        'title',
        'category',
        'author',
        'is_published',
        'created_at',
        'get_reading_time',
    )
    list_filter = (
        'category',
        'is_published',
        'created_at',
    )
    search_fields = (
        'title',
        'content',
    )
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    actions = ['publish_posts', 'unpublish_posts']

    @admin.display(description="Reading Time")
    def get_reading_time(self, obj):
        return f"{obj.reading_time} min"

    @admin.action(description="Mark selected posts as Published")
    def publish_posts(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} post(s) successfully marked as published.")

    @admin.action(description="Mark selected posts as Draft (Unpublished)")
    def unpublish_posts(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} post(s) successfully marked as draft.")
