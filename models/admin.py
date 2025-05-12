from django.contrib import admin
from .models import MLModel, TrainTestData

# Register your models here.
@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'model_type',)
    
admin.site.register(TrainTestData)