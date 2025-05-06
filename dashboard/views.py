from django.shortcuts import render
import pandas as pd

df = pd.read_csv('data\data.csv')

# Create your views here.
def home(request):
    columns = df.columns.tolist()

    context = {
        'columns': columns
    }
    return render(request, 'dashboard/dashboard.html', context)
