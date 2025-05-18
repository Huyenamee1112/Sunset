from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from upload.models import Dataset


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
    

class ProfileUpdateForm(forms.ModelForm):
    dataset = forms.ModelChoiceField(
        queryset=Dataset.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['dataset'].queryset = Dataset.objects.filter(user=self.user)
            self.fields['dataset'].initial = self.instance.dataset
            
    class Meta:
        model = Profile
        fields = ['dataset']
        
    def save(self, commit=True):
        profile = self.instance
        profile.dataset = self.cleaned_data['dataset']
        
        if commit:
            profile.save()
        return profile
    

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'readonly': 'readonly'
    }))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']