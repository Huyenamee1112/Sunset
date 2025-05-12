from django.shortcuts import render, get_object_or_404, redirect
from upload.models import Dataset
from django.contrib.auth.decorators import login_required
import csv
import itertools

# Create your views here.
@login_required
def dataset_list(request):
    datasets = Dataset.objects.filter(user=request.user)
    return render(request, 'list/list.html', {'datasets': datasets})

@login_required
def dataset_delete(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    dataset.delete()
    return redirect('dataset_list')


@login_required
def csv_view(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)

    file_path = dataset.file.path
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            csv_data = list(itertools.islice(reader, 20))
    except FileNotFoundError:
        return render(request, 'list/data_view.html', {'error': 'File not found.'})
    except Exception as e:
        return render(request, 'list/data_view.html', {'error': f'Error reading file: {str(e)}'})

    return render(request, 'list/data_view.html', {
        'csv_data': csv_data,
        'dataset': dataset
    })