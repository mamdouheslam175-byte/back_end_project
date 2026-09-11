from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Category, Post

POSTS_PER_PAGE = 5


def _paginate_posts(queryset, request, per_page=POSTS_PER_PAGE):
    """
    Helper function to paginate posts and handle out-of-range pages gracefully.
    Handles PageNotAnInteger and EmptyPage as required by Story 8.
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer (or not provided), deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results
        page_obj = paginator.page(paginator.num_pages)

    return page_obj, paginator


def post_list(request):
    """
    Story 5: Homepage function-based view querying is_published=True ordered by newest first.
    Story 8: Pagination using Django's Paginator (5 posts per page).
    Bonus: Search bar filtering using Q objects (title and content).
    """
    query = request.GET.get('q', '').strip()
    posts = Post.objects.filter(is_published=True).select_related('category', 'author').order_by('-created_at')

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    page_obj, paginator = _paginate_posts(posts, request)

    context = {
        'page_obj': page_obj,
        'paginator': paginator,
        'posts': page_obj.object_list,
        'query': query,
        'is_category_view': False,
        'page_title': f'Search results for "{query}"' if query else 'Latest Stories & Insights',
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """
    Story 6: Post detail function-based view using slug (/post/<slug>/),
    get_object_or_404, and returning 404 if is_published=False.
    """
    # Fetch post or 404
    post = get_object_or_404(Post, slug=slug)

    # Ensure unpublished posts return 404
    if not post.is_published:
        raise Http404("This post is not published.")

    # Related posts from the same category for enhanced UX
    related_posts = (
        Post.objects.filter(category=post.category, is_published=True)
        .exclude(pk=post.pk)
        .order_by('-created_at')[:3]
    )

    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


def category_posts(request, slug):
    """
    Story 7: Category filter function-based view using category slug (/category/<slug>/),
    filtering published posts by category, and reusing the post_list.html template structure.
    Story 8: Pagination (5 posts per page) handling PageNotAnInteger & EmptyPage.
    """
    category = get_object_or_404(Category, slug=slug)
    query = request.GET.get('q', '').strip()

    posts = Post.objects.filter(
        category=category,
        is_published=True
    ).select_related('category', 'author').order_by('-created_at')

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    page_obj, paginator = _paginate_posts(posts, request)

    context = {
        'page_obj': page_obj,
        'paginator': paginator,
        'posts': page_obj.object_list,
        'category': category,
        'query': query,
        'is_category_view': True,
        'page_title': f'{category.name} Articles',
    }
    return render(request, 'blog/post_list.html', context)
