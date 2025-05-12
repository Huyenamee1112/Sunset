from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from upload.models import Dataset
from models.models import MLModel
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .import process
import pandas as pd
from sklearn import metrics
import pickle

# Create your views here.
@login_required
def predict_view(request):
    datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
    try:
        admin = User.objects.get(username='admin')
    except:
        pass
    
    context = {
        'datasets': datasets,
        'models': MLModel.objects.filter(user__in=[request.user, admin])
    }
    return render(request, 'predict/predict.html', context)


# /api/predict/
@csrf_exempt
def predict_api(request):
    if request.method == 'POST':
        try:
            dataset_name = request.POST.get('dataset')
            model_name = request.POST.get('model')
            validation_file = request.FILES.get('validation_file')
            
            # load data
            try:
                dataset = Dataset.objects.get(name=dataset_name)
                processed_data_path = dataset.processed_data.file.path
                df = pd.read_csv(processed_data_path)
                X = process.get_processed_data(df)
                
            except Dataset.DoesNotExist as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

            # Load model
            try:
                model_instance = MLModel.objects.get(name=model_name)
                
                with model_instance.file.open('rb') as f:
                    model = pickle.load(f)
                    
            except MLModel.DoesNotExist as e:
                return JsonResponse({'error': str(e)}, status=400)

            # Predict
            y_pred = model.predict(X)
            y_pred_prob = model.predict_proba(X)[:, 1] if hasattr(model, "predict_proba") else [None] * len(y_pred)
            
            response_data = {
                'y_pred': y_pred.tolist(),
                'y_pred_prob': [float(p) if p is not None else None for p in y_pred_prob],
            }

            # If validation file provided, calculate metrics
            if validation_file:
                val_df = pd.read_csv(validation_file)

                # Assume y_true is the last column
                y_true = val_df.iloc[:, -1]

                result = {
                    'Accuracy': round(metrics.accuracy_score(y_true, y_pred), 4),
                    'Precision': round(metrics.precision_score(y_true, y_pred, zero_division=0), 4),
                    'Recall': round(metrics.recall_score(y_true, y_pred, zero_division=0), 4),
                    'F1 Score': round(metrics.f1_score(y_true, y_pred, zero_division=0), 4),
                }

                response_data['validation_metrics'] = result

            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)