from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden

def index(request):
    articles = Article.objects.all()
    titles = []
    contents = []
    for i in articles:
        titles.append(i.title)
        contents.append(i.content)
    context = {
        'articles': articles,
        'titles': titles,
        'contents': contents,
    }
    return render(request, 'articles/index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm()
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
    return render(request, 'articles/detail.html', context)


@require_POST
def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.user == article.user:
        article.delete()
        return redirect('articles:index')
    else:
        messages.warning(request, '허가된 사용자가 아닙니다.')
        return HttpResponseForbidden()



def update(request, article_pk):
    article = Article.objects.get(id=article_pk)
    if article.user == request.user:
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
    else:
        return HttpResponseForbidden()


def comment_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.article = article
        comment.save()
    else:
        messages.success(request, '댓글의 형식이 맞지 않습니다.')
    return redirect('articles:detail', article.pk)


@require_POST
def comment_delete(request, article_pk, comment_id):
    article = Article.objects.get(pk=article_pk)
    comment = Comment.objects.get(pk=comment_id)
    if comment.user == request.user:
        comment.delete()
        article.save()
        messages.success(request, '댓글이 삭제되었습니다.')
        return redirect('articles:detail', article.pk)
    else:
        return HttpResponseForbidden()

@login_required
def like(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)
    return redirect('articles:detail', article_pk)

    