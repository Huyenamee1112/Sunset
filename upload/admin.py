from django.contrib import admin
from .models import Dataset, ProcessedData

# Register your models here.
@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user')
    
admin.site.register(ProcessedData)