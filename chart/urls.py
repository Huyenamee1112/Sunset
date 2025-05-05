from django.urls import path
from . import views

urlpatterns = [
    path('chart-apex/', views.chart_apex, name='chart_apex'),
]