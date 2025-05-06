from django.shortcuts import render
from .models import StatsResult
from django.http import JsonResponse
import pandas as pd
import io

# Create your views here.
df = pd.read_csv('data\data.csv')


def get_stats(request):
    record = StatsResult.objects.get(pk=1)
    return JsonResponse(record.stats_data)
    
    

def frequent_chart(request):
    column = request.GET.get("column")
    if column not in df.columns:
        return JsonResponse({"error": "Invalid column"}, status=400)

    top_n = 10
    counts = df[column].value_counts().nlargest(top_n).to_dict()
    
    labels = [str(k) for k in counts.keys()]
    values = list(counts.values())

    return JsonResponse({
        "labels": labels,
        "values": values
    })


def ctr_chart(request):
    group_column = request.GET.get("column")
    if group_column not in df.columns:
        return JsonResponse({"error": "Invalid column"}, status=400)

    try:
        group_data = df.groupby([group_column, 'click']).size().unstack()
    except Exception:
        return JsonResponse({"error": "Grouping error"}, status=400)

    group_data['Frequency'] = df[group_column].value_counts(normalize=True).round(2)
    group_data['CTR'] = (group_data.get(1, 0) / (group_data.get(0, 0) + group_data.get(1, 0))).round(2)
    group_data = group_data.fillna(0)
    
    top_n = 10
    group_data = group_data.sort_values(by='CTR', ascending=False).head(top_n)

    return JsonResponse({
        "labels": [str(idx) for idx in group_data.index],
        "frequency": group_data['Frequency'].tolist(),
        "ctr": group_data['CTR'].tolist()
    })


def pie_chart(request):
    column = request.GET.get("column")
    
    if not column:
        return JsonResponse({"error": "Column parameter is required"}, status=400)

    if column not in df.columns:
        return JsonResponse({"error": f"Column '{column}' not found in the dataset"}, status=400)

    top_n = 20
    counts = df[column].value_counts().nlargest(top_n).to_dict()
    
    labels = [str(k) for k in counts.keys()]
    values = list(counts.values())

    return JsonResponse({
        "labels": labels,
        "values": values
    })
    
    
    
def heatmap_chart(request):
    corr = df.select_dtypes(include=['number']).corr()
    categories = list(corr.columns)

    heatmap_data = []

    for i, row_name in enumerate(categories):
        row = {
            "name": row_name,
            "data": []
        }
        for j, col_name in enumerate(categories):
            row["data"].append({
                "x": col_name,
                "y": round(corr.iloc[i, j], 2)
            })
        heatmap_data.append(row)

    return JsonResponse({
        "categories": categories,
        "series": heatmap_data
    })


def analytics_info(request):
    info_html = "<table class='table table-striped'><thead><tr><th>Column</th><th>Non-Null Count</th><th>Dtype</th></tr></thead><tbody>"

    for column in df.columns:
        non_null_count = df[column].notnull().sum()
        dtype = df[column].dtype
        info_html += f"<tr><td>{column}</td><td>{non_null_count}</td><td>{dtype}</td></tr>"

    info_html += "</tbody></table>"

    return JsonResponse({"info_html": info_html})



def data_summary(request):
    description = df.describe().transpose()
    
    summary = {}
    for column, stats in description.iterrows():
        summary[column] = {
            "count": stats['count'],
            "mean": stats['mean'],
            "std": stats['std'],
            "min": stats['min'],
            "25_percent": stats['25%'],
            "50_percent": stats['50%'],
            "75_percent": stats['75%'],
            "max": stats['max']
        }
    
    return JsonResponse({"description": summary})