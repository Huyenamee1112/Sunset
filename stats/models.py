from django.db import models
from upload.models import Dataset

# Create your models here.
class StatsResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    stats_data = models.JSONField()
    
    def __str__(self):
        return str(self.pk)