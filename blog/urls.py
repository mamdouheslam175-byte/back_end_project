from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Story 5: Homepage displaying newest published posts
    path('', views.post_list, name='post_list'),

    # Story 6: Detail page displaying single post with 404 for unpublished/missing
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),

    # Story 7: Category filter displaying published posts in that category
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
]
