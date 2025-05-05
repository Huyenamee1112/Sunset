from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
from django.conf import settings
from .models import Dataset

@receiver(pre_delete, sender=Dataset)
def delete_file(sender, instance, **kwargs):
    if instance.file:
        file_path = instance.file.path
        if os.path.isfile(file_path):
            os.remove(file_path)
