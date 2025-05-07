from django.urls import path
from .import views

urlpatterns = [
    path('api/frequent-chart/', views.frequent_chart, name='frequent_chart'),
    path('api/ctr-chart/', views.ctr_chart, name='ctr_chart'),
    path('api/pie-chart/', views.pie_chart, name='pie_chart'),
    path('api/heatmap-chart/', views.heatmap_chart, name='heatmap_chart'),
    path('api/analytics-info/', views.analytics_info, name='analytics_info'),
    path('api/data-summary/', views.data_summary, name='data_summary'),
    path('api/boxplot-data/', views.boxplot_data, name='boxplot_data'),
    path('api/click-vs-non-click-ctr/', views.click_vs_non_click_ctr, name='click_vs_non_click_ctr'),
    path('api/scatter-plot/', views.scatter_plot_data, name='scatter-plot'),
]