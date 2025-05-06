from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
import os
from django.conf import settings
from .models import Dataset
import pandas as pd
from stats.stats import get_stats
from stats.models import StatsResult

@receiver(pre_delete, sender=Dataset)
def delete_file(sender, instance, **kwargs):
    if instance.file:
        file_path = instance.file.path
        if os.path.isfile(file_path):
            os.remove(file_path)
            
            
@receiver(post_save, sender=Dataset)
def process(sender, instance, created, **kwargs):
    if created:
        df = pd.read_csv(instance.file)
        stats = get_stats(df)
        StatsResult.objects.create(stats_data=stats)