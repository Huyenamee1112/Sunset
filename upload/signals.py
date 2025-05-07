from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import Dataset, ProcessedData
import os
import pandas as pd
from .utils import processed_dataset
from django.core.files.base import ContentFile
from io import StringIO

@receiver(pre_delete, sender=Dataset)
def delete_file(sender, instance, **kwargs):
    if instance.file:
        file_path = instance.file.path
        processed_path = instance.processed_data.file.path
        if os.path.isfile(file_path):
            os.remove(file_path)
        if os.path.isfile(processed_path):
            os.remove(processed_path)
            
            
@receiver(post_save, sender=Dataset)
def created_processed_data(sender, instance, created, **kwargs):
    if created:
        file_path = instance.file.path
        df = pd.read_csv(file_path)
        try:
            processed_df = processed_dataset(df)
            
            csv_buffer = StringIO()
            processed_df.to_csv(csv_buffer, index=False)
            csv_content = csv_buffer.getvalue()
            
            name = f'{instance.name}_processed.csv'
            
            csv_model_instance = ProcessedData(name=name, dataset=instance)
            csv_model_instance.file.save(name, ContentFile(csv_content))
            csv_model_instance.save()
            
        except Exception as e:
            print('An exception while processing dataset.')