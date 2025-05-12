from django.urls import path
from .import views

urlpatterns = [
    path('predict/', views.predict_view, name='predict_view'),
    path('api/predict/', views.predict_api, name='predict_api')
]