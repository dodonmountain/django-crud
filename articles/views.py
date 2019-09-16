from django.shortcuts import render, redirect
from .models import Article, Comment
from django.views.decorators.http import require_POST


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
        'articles':  article
    }
    # return render(request, 'articles/create.html', context)
    return redirect('articles:detail', article.pk)

def detail(request, article_pk):
    articles = Article.objects.get(pk=article_pk)
    comments = articles.comment_set.all()
    context = {
        'articles': articles,
        'comments': comments,
    }
    return render(request, 'articles/detail.html',context)

@require_POST
def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        article.delete()
        return redirect('articles:index')
    # else:
    #     return redirect('articles:index')
def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {
        'articles':article,
    }
    return render(request, 'articles/update.html', context)

def upd(request, article_pk):
    tb = request.POST.get('tb')
    th = request.POST.get('th')
    article = Article.objects.get(pk=article_pk)
    article.content = tb
    article.title = th
    article.save()
    return redirect('articles:index')

def comment_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    c_content = request.POST.get('comment')
    comment = Comment()
    comment.content = c_content
    comment.article = article
    comment.save()
    return redirect('articles:detail', article.pk)