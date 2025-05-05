from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DatasetUploadForm

# Create your views here.
@login_required
def upload_view(request):
    if request.method == 'POST':
        form = DatasetUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('upload')
        else:
            print(form.errors)
    else:
        form = DatasetUploadForm(user=request.user)
        
    return render(request, 'upload/upload.html', {'form': form})