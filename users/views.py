from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import login, logout

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = UserLoginForm()
        
    return render(request, 'users/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
        
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')