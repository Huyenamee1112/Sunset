from django.db import models

# Create your models here.
MODEL_CHOICES = [
    ('decision_tree', 'Decision Tree Classifier'),
    ('random_forest', 'Random Forest Classifier'),
    ('xgboost', 'XGBoost Classifier')
]

class MLModel(models.Model):
    name = models.CharField(max_length=32, unique=True)
    model_type = models.CharField(max_length=32, choices=MODEL_CHOICES, default='decision_tree')
    file = models.FileField(upload_to='models/')

    def __str__(self):
        return self.name