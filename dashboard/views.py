from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'dashboard/dashboard.html')


def analytics(request):
    return render(request, 'dashboard/analytics.html')