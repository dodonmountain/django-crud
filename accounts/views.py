from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

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