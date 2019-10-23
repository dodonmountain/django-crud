from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.http import HttpResponseForbidden


def signup(request):
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
    return render(request, 'accounts/form.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # 로그인
            user = form.get_user()
            auth_login(request, user)
            # 단축평가 활용 NONE 리턴시
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('articles:index')

# @login_required
# def update(request):
#     form = UserChangeForm(request.POST)
#     if form.is_valid():
#         account = form.save()
#         return redirect('admin')
#     else:
#         form = UserChangeForm(request.POST)


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)


@login_required
def password_change(request):
    if request.method == 'POST':
        # 반드시 첫번째 인자로 user 객체를 사용
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)


@login_required
def profile(request, account_pk):
    user = get_object_or_404(get_user_model(), pk=account_pk)
    # if account_pk == request.user.pk:
    context = {
        'user_profile': user,
    }
    return render(request, 'accounts/profile.html', context)

def follow(request, account_pk):
    f_user = get_object_or_404(get_user_model(), pk=account_pk)
    if f_user != request.user:
        if request.user in f_user.followers.all(): 
            f_user.followers.remove(request.user)
        else:
            f_user.followers.add(request.user)
    return redirect('accounts:profile', account_pk)