from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from upload.models import Dataset
from .models import MODEL_CHOICES
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time

# Create your views here.
@login_required
def machine_learning(request):
    datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
    model_choices = {
        x[0]: x[1] for x in MODEL_CHOICES
    }
    context = {
        'datasets': datasets,
        'model_choices': model_choices
    }
    return render(request, 'models/models.html', context)


@csrf_exempt
def training_api(request):
    if request.method == "POST":
        try:
            dataset_name = request.POST.get('dataset')
            selected_model = request.POST.get('model')
            model_name = request.POST.get('model_name')
            params_json = request.POST.get('params')
            
            print(params_json)

            if not all([dataset_name, selected_model, model_name, params_json]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            try:
                params = json.loads(params_json)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON in parameters'}, status=400)

            # --- Placeholder xử lý training ---
            # print(dataset_name, selected_model, model_name, params_json)
            time.sleep(5)

            
            return JsonResponse({
                'message': 'Training started successfully',
                'dataset': dataset_name,
                'model': selected_model,
                'model_name': model_name,
                'params': params
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
    