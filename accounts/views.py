from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# Create your views here.

def signup(request):
    if request.method == 'POST':
        uc_form = UserCreationForm(request.POST)
        if uc_form.is_valid():
            account = uc_form.save()
            return redirect('articles:index')
    else:
        uc_form = UserCreationForm()
    context = {
        'uc_form':uc_form,
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # 로그인
            user = form.get_user()
            auth_login(request, user)
            return redirect(request.GET.get('next') or 'articles:index') #단축평가 활용 NONE 리턴시 
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('articles:index')