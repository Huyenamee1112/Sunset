from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from upload.models import Dataset
from .models import MODEL_CHOICES
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import time
from .utils import create_train_test_data, training, testing
from .models import MLModel
from django.contrib.auth.models import User

# Create your views here.
@login_required
def machine_learning(request):
    datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
    model_choices = {
        x[0]: x[1] for x in MODEL_CHOICES
    }
    
    context = {
        'datasets': datasets,
        'model_choices': model_choices,
        'models': MLModel.objects.filter(user=request.user)
    }
    return render(request, 'models/models.html', context)

@login_required
def model_list_view(request):
    context = {
        'models': MLModel.objects.filter(user=request.user)
    }
    return render(request, 'models/model_list_view.html', context)


@login_required
def model_delete(request, model_id):
    dataset = get_object_or_404(MLModel, id=model_id)
    dataset.delete()
    return redirect('model_list_view')
 

@csrf_exempt
def training_api(request):
    if request.method == "POST":
        try:
            dataset_name = request.POST.get('dataset')
            selected_model = request.POST.get('model')
            model_name = request.POST.get('model_name')

            if not all([dataset_name, selected_model, model_name]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            if MLModel.objects.filter(user=request.user, name=model_name).exists():
                return JsonResponse({'error': 'Model name already exists.'}, status=400)

            # --- Placeholder xử lý training ---
            try:
                dataset = Dataset.objects.get(user=request.user, name=dataset_name)
                if not hasattr(dataset, 'train_test_data'):
                    processed_data_path = dataset.processed_data.file.path
                    create_train_test_data(dataset, processed_data_path)
                
            except Dataset.DoesNotExist:
                return JsonResponse({'error': 'Dataset does not exists.'}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': str(e)}, status=400)
            
            
            # train
            try:
                training(request.user, dataset_name, selected_model, model_name)
            except Exception as e:
                return JsonResponse({'error': f'An error while training model({str(e)}).'}, status=400)

            
            return JsonResponse({
                'message': 'Training started successfully',
                'dataset': dataset_name,
                'model': selected_model,
                'model_name': model_name,
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    
@csrf_exempt
def testing_api(request):
    if request.method == "POST":
        try:
            dataset_name = request.POST.get('dataset')
            model_name = request.POST.get('model_name')

            if not all([dataset_name, model_name]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            

            # --- Placeholder xử lý training ---
            try:
                dataset = Dataset.objects.get(user=request.user, name=dataset_name)
                if not hasattr(dataset, 'train_test_data'):
                    processed_data_path = dataset.processed_data.file.path
                    create_train_test_data(dataset, processed_data_path)
                
            except Dataset.DoesNotExist:
                return JsonResponse({'error': 'Dataset does not exists.'}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': str(e)}, status=400)
            
            # Testing
            try:
                result = testing(dataset_name, model_name)
            except Exception as e:
                return JsonResponse({'error': f'An error while training model({str(e)}).'}, status=400)
            
            return JsonResponse({
                'message': 'Training started successfully',
                'dataset': dataset_name,
                'model_name': model_name,
                'result': result
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)