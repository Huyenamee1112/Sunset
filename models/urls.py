from django.urls import path
from . import views

urlpatterns = [
    path('models/', views.machine_learning, name='models'),
    path('api/training/', views.training_api, name='training_api'),
    path('api/testing/', views.testing_api, name='testing_api'),
    path('models/list-view/', views.model_list_view, name='model_list_view'),
    path('model-delete/<int:model_id>/', views.model_delete, name='model_delete')
]