from pages.models import Page

def get_pages(request):
    
    pages = Page.objects.values_list('id', 'title', 'slug')             # devuelve un objeto de tipo pages
    #pages = Page.objects.values_list('title', flat = True)             # Devuelve los elemento en texto plano
    #pages = Page.objects.filter(visible=True).values_list('title', flat = True)             # Devuelve los elementos de las paginas que son visibles
    return {
        'pages': pages
    }