from django.urls import path
from . import views

urlpatterns = [
    path('datasets/', views.dataset_list, name='dataset_list'),
    path('datasets/delete/<int:dataset_id>/', views.dataset_delete, name='dataset_delete'),
    path('datasets/csv-view/<int:dataset_id>/', views.csv_view, name='csv_view'),
]