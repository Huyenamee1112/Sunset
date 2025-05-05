from django.contrib import admin
from .models import Dataset

# Register your models here.
@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    search_fields = ('user', 'name')