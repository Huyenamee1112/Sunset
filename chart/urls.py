from django.urls import path
from . import views

urlpatterns = [
    path('chart-apex/', views.chart_apex, name='chart_apex'),
    path('map-vector/', views.map_vector, name='map_vector')
]