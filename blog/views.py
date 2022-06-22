from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from blog.models import Category, Article
from django.contrib.auth.decorators import login_required           # exporta la funcion que atentica previo a entrar a la url

# Create your views here.

@login_required(login_url="login")
def list(request):
		
	# Sacar articulos
	articles = Article.objects.all()
	
	# Paginar articulos
	paginator = Paginator(articles, 2)						# el 2 define la cantidad de objetos por pagina
	
	# Recoger numero pagina
	page = request.GET.get('page')							# Recibe, desde la web el numero de pagina actual
	page_articles = paginator.get_page(page)
	
	return render(request, 'articles/list.html', {
		'title': 'Articulos',
        'articles': page_articles
	})


def category(request, category_id):
    
    #category = Category.objects.get(id=category_id)
    category = get_object_or_404(Category, id=category_id)
    articles = Article.objects.filter(categories=category_id)
    
    return render(request, 'categories/category.html',{
        'category': category,
        'articles': articles
    })
    
def article(request, article_id):
    
    article = get_object_or_404(Article, id=article_id)
    
    return render(request, 'articles/detail.html', {
        'article' : article,
    })