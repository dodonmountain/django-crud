from django.shortcuts import render, redirect
from .models import Article
# Create your views here.
def index(request):
    articles = Article.objects.all()
    titles = []
    contents = []
    for i in articles:
        titles.append(i.title)
        contents.append(i.content)

    context = {
        'articles': articles,
        'titles' : titles,
        'contents' : contents,
    }
    return render(request, 'articles/index.html', context)

def new(request):
    return render(request, 'articles/new.html')

def create(request):
    th = request.POST.get('th')
    tb = request.POST.get('tb')
    article = Article.objects.create(title=th, content=tb)
    context = {
        'article':  article
    }
    # return render(request, 'articles/create.html', context)
    return redirect(f'/articles/{article.pk}/')

def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {
        'article': article
    }
    return render(request, 'articles/detail.html', context)

def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    article.delete()
    return redirect('/articles/')