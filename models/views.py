from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from upload.models import Dataset

# Create your views here.
@login_required
def machine_learning(request):
    datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
    context = {
        'datasets': datasets
    }
    return render(request, 'models/models.html', context)