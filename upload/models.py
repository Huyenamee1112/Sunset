from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Dataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dataset')
    name = models.CharField(max_length=255, unique=True)
    file = models.FileField(upload_to='upload/users/dataset/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name