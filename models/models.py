from django.db import models
from django.contrib.auth.models import User
from upload.models import Dataset

# Create your models here.
MODEL_CHOICES = [
    ('logistic_regression', 'Logistic Regression'),
    ('catboost', 'CatBoost Classifier'),
    ('random_forest', 'Random Forest Classifier'),
    ('decision_tree', 'Decision Tree Classifier'),
    ('xgboost', 'XGBoost Classifier')
]

class MLModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ml_model')
    name = models.CharField(max_length=255, unique=True)
    model_type = models.CharField(max_length=32, choices=MODEL_CHOICES, default='logistic_regression')
    file = models.FileField(upload_to='models/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class TrainTestData(models.Model):
    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE, related_name='train_test_data')
    X_train = models.FileField(upload_to='upload/users/train_test_data/')
    X_test = models.FileField(upload_to='upload/users/train_test_data/')
    y_train = models.FileField(upload_to='upload/users/train_test_data/')
    y_test = models.FileField(upload_to='upload/users/train_test_data/')
    
    def __str__(self):
        return f'{self.dataset.name} modeling'
    
