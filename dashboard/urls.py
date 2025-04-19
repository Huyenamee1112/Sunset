from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.home, name='home'),
    path('analytics/', views.analytics, name='analytics'),
    
    # api
    path('api/dashboard-data/', api.chart_data, name='chart-data')
]