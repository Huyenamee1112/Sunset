from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
    
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise forms.ValidationError('Username or password is not correct.')
        
        self.user = user
        
        return password


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password'
    }), label='Confirm Password')
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
