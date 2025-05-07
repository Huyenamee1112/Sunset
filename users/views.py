from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, logout
from django.contrib import messages
from users.models import Profile
from django.contrib.auth.decorators import login_required

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

@login_required
def profile(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = None
        
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, user=request.user, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Profile upload failed!')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(user=request.user, instance=user_profile)
    
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }    
    
    return render(request, 'users/profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')