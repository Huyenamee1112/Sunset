from django.urls import path
from .import views

urlpatterns = [
    path('get-stats/', views.get_stats, name='get_stats'),
    path('api/frequent-chart/', views.frequent_chart, name='frequent_chart'),
    path('api/ctr-chart/', views.ctr_chart, name='ctr_chart'),
    path('api/pie-chart/', views.pie_chart, name='pie_chart'),
    path('api/heatmap-chart/', views.heatmap_chart, name='heatmap_chart'),
    path('api/analytics-info/', views.analytics_info, name='analytics_info'),
    path('api/data-summary/', views.data_summary, name='data_summary'),
]