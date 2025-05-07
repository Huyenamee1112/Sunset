from django.urls import path
from . import views

urlpatterns = [
    path('models/', views.machine_learning, name='models'),
    path('api/training/', views.training_api, name='training_api'),
]