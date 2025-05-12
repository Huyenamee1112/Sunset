from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import TrainTestData
import os

@receiver(pre_delete, sender=TrainTestData)
def delete_file(sender, instance, **kwargs):
    if instance:
        X_train_file = instance.X_train.path
        X_test_file = instance.X_test.path
        y_train_file = instance.y_train.path
        y_test_file = instance.y_test.path
        if os.path.isfile(X_train_file):
            os.remove(X_train_file)
        if os.path.isfile(X_test_file):
            os.remove(X_test_file)
        if os.path.isfile(y_train_file):
            os.remove(y_train_file)
        if os.path.isfile(y_test_file):
            os.remove(y_test_file)