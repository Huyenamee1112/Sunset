from django.shortcuts import render
from stats.utils import get_df
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    df = get_df(request.user.id)
    columns = []
    if df is not None:
        columns = df.columns.tolist()

    context = {
        'columns': columns
    }
    return render(request, 'dashboard/dashboard.html', context)
