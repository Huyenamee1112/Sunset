from django import forms
from .models import Dataset

class DatasetUploadForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Dataset Name'
    }))
    file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control'
    }), label='Choose File')
    
    class Meta:
        model = Dataset
        fields = ['name', 'file']
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and ' ' in name:
            raise forms.ValidationError('Name must not contain space character.')
        return name
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance