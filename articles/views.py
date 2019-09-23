# from IPython import embed
from django.shortcuts import render, redirect
from .models import Article, Comment
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import ArticleForm, CommentForm

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

# def new(request):
#     return render(request, 'articles/new.html')

def create(request):
    if request.method == 'POST':
        # th = request.POST.get('th')
        # tb = request.POST.get('tb')
        article_form = ArticleForm(request.POST)
        # validation
        if article_form.is_valid():
            article = article_form.save()
            return redirect('articles:detail', article.pk)
    else:
    # GET 요청 -> Form
        article_form = ArticleForm()
    # GET -> 비어있는 Form context
    # POST -> 검증 실패시 에러메세지와 입력값 채워진 form context
    context = {
        'article_form':  article_form,
    }
    return render(request, 'articles/form.html', context)

def detail(request, article_pk):
    articles = Article.objects.get(pk=article_pk)
    comments = articles.comment_set.all()
    comment_form = CommentForm(request.POST)
    context = {
        'articles': articles,
        'comments': comments,
        'comment_form': comment_form,
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
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article = article_form.save()
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        'article_form':  article_form,
    }
    return render(request, 'articles/form.html', context)

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
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.save()
    else:
        messages.success(request, '댓글의 형식이 맞지 않습니다.')
    return redirect('articles:detail', article.pk)

@require_POST
def comment_delete(request, article_pk, comment_id):
    article = Article.objects.get(pk=article_pk)
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    article.save()
    messages.success(request, '댓글이 삭제되었습니다.')
    return redirect('articles:detail', article.pk)

