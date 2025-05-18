from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from upload.models import Dataset
from models.models import MLModel
from django.views.decorators.csrf import csrf_exempt
from .import process
import pandas as pd
from sklearn import metrics
from django.http import HttpResponse, JsonResponse
import pickle
import csv

# Create your views here.
@login_required
def predict_view(request):
    datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
    
    context = {
        'datasets': datasets,
        'models': MLModel.objects.filter(user=request.user)
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
            output_format = request.GET.get('format', 'json')  # lấy param format (mặc định json)
            
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

            # Nếu có validation file, đọc y_true
            y_true = None
            if validation_file:
                # Đọc file TXT upload (giữ header=None nếu không có header)
                val_df = pd.read_csv(validation_file, header=None)
                y_true = val_df.iloc[:, -1]
                result = {
                    'Accuracy': round(metrics.accuracy_score(y_true, y_pred), 4),
                    'Precision': round(metrics.precision_score(y_true, y_pred, zero_division=0), 4),
                    'Recall': round(metrics.recall_score(y_true, y_pred, zero_division=0), 4),
                    'F1 Score': round(metrics.f1_score(y_true, y_pred, zero_division=0), 4),
                }
            else:
                result = None

            if output_format.lower() == 'txt':
                # Trả về file TXT
                response = HttpResponse(content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename="prediction_results.txt"'

                writer = csv.writer(response, delimiter='\t')  # dùng tab để dễ đọc txt
                # Header
                header = ['y_pred', 'y_pred_prob']
                if y_true is not None:
                    header.append('y_true')
                writer.writerow(header)

                # Dữ liệu từng dòng
                for i in range(len(y_pred)):
                    row = [y_pred[i], float(y_pred_prob[i]) if y_pred_prob[i] is not None else None]
                    if y_true is not None:
                        row.append(y_true.iloc[i])
                    writer.writerow(row)

                return response
            else:
                # Trả về JSON
                response_data = {
                    'y_pred': y_pred.tolist(),
                    'y_pred_prob': [float(p) if p is not None else None for p in y_pred_prob],
                }
                if result:
                    response_data['validation_metrics'] = result

                return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
