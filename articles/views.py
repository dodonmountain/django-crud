from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ArticleForm, CommentForm
from .models import Article, Comment, HashTag
from django.contrib.auth import login as auth_login
from django.http import HttpResponseForbidden,JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import CustomUserCreationForm


def index(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
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
            # 해쉬태그 저장 및 연결
            for word in article.content.split():
                if word.startswith('#'):
                    hashtag, created = HashTag.objects.get_or_create(
                        content=word)
                    article.hashtags.add(hashtag)
                return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm()
    context = {
        'article_form':  article_form,
    }
    return render(request, 'articles/form.html', context)

def detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    articles = get_object_or_404(Article, pk=article_pk)
    comments = articles.comment_set.all()
    comment_form = CommentForm()
    context = {
        'articles': articles,
        'comments': comments,
        'comment_form': comment_form
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
                article.hashtags.clear()
                for word in article.content.split():
                    if word.startswith('#'):
                        hashtag, created = HashTag.objects.get_or_create(
                            content=word)
                        article.hashtags.add(hashtag)
                    return redirect('articles:detail', article.pk)
        else:
            article_form = ArticleForm(instance=article)
        context = {
            'article_form':  article_form,
        }
        return render(request, 'articles/form.html', context)
    else:
        return HttpResponseForbidden()


@login_required
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
    is_liked = False
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        is_liked = False
    else:
        article.like_users.add(request.user)
        is_liked = True
    count = article.like_users.count()
    context ={
        'is_liked': is_liked,
        'count':count,
    }
    return JsonResponse(context)


def hashtag(request, hashtag_pk):
    hashtag = get_object_or_404(HashTag, pk=hashtag_pk)
    context = {
        'hashtag': hashtag,
    }
    return render(request, 'articles/hashtag.html', context)

def explore(request):
    from itertools import chain
    followings = request.user.followings.all()
    followings = chain(followings, [request.user])
    articles = Article.objects.filter(user_in=followings).order_by('created_at')
    context = {
        'articles':articles
    }
    return render(request, 'articles')