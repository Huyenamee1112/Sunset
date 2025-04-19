from django.shortcuts import render

# Create your views here.
def chart_apex(request):
    return render(request, 'chart/chart-apex.html')

def map_vector(request):
    return render(request, 'chart/map-vector.html')