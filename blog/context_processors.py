from .models import Category


def categories_processor(request):
    """
    Context processor to make all categories accessible across all templates,
    enabling global navigation without redundant querying in each view.
    """
    return {
        'all_categories': Category.objects.all().order_by('name')
    }
