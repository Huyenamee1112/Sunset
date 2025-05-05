from django.db import models
from django.contrib.auth.models import User
from upload.models import Dataset

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='users/donate.jpg', upload_to='users/')
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='profile', blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
