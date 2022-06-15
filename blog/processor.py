from blog.models import Category, Article

def get_categories(request):
    
    categories_in_use = Article.objects.filter(public=True).values_list('categories', flat=True)
    categories = Category.objects.filter(id__in=categories_in_use).values_list('id', 'name')     # id__in : Significa id "que estan en" categories_in_use

    return {
        'categories': categories,
    }