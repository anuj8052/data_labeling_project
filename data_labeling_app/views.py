from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import FileUploadForm, LabelEditForm
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans, DBSCAN
import json
import os
from django.conf import settings
from plotly.utils import PlotlyJSONEncoder
from django.http import HttpResponse

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage(location=settings.UPLOAD_FOLDER)
            filename = fs.save(file.name, file)
            return redirect('label_data', filename=filename)
    else:
        form = FileUploadForm()
    return render(request, 'data_labeling_app/upload.html', {'form': form})

# def label_data(request, filename):
#     file_path = os.path.join(settings.UPLOAD_FOLDER, filename)
#     if not os.path.exists(file_path):
#         return render(request, 'data_labeling_app/error.html', {'message': 'File not found.'})
    
#     df = pd.read_csv(file_path)
#     fig = px.scatter(df, x=df.columns[0], y=df.columns[1])
#     graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
    
#     if request.method == 'POST':
#         form = LabelEditForm(request.POST)
#         if form.is_valid():
#             index = form.cleaned_data['index']
#             label = form.cleaned_data['label']
#             df.at[index, 'label'] = label
#             df.to_csv(file_path, index=False)
#             return redirect('label_data', filename=filename)
#     else:
#         form = LabelEditForm()
    
#     return render(request, 'data_labeling_app/labeling.html', {'graph_json': graph_json, 'filename': filename, 'form': form})

def label_data(request, filename):
    file_path = os.path.join(settings.UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return render(request, 'data_labeling_app/error.html', {'message': 'File not found.'})
    
    df = pd.read_csv(file_path)
    fig = px.scatter(df, x=df.columns[0], y=df.columns[1], color='cluster' if 'cluster' in df.columns else None)
    graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
    
    if request.method == 'POST':
        form = LabelEditForm(request.POST)
        if form.is_valid():
            index = form.cleaned_data['index']
            label = form.cleaned_data['label']
            df.at[index, 'label'] = label
            df.to_csv(file_path, index=False)
            return redirect('label_data', filename=filename)
    else:
        form = LabelEditForm()
    
    return render(request, 'data_labeling_app/labeling.html', {'graph_json': graph_json, 'filename': filename, 'form': form})

# def cluster_data(request, filename):
#     file_path = os.path.join(settings.UPLOAD_FOLDER, filename)
#     if not os.path.exists(file_path):
#         return render(request, 'data_labeling_app/error.html', {'message': 'File not found.'})
    
#     df = pd.read_csv(file_path)
#     algorithm = request.POST.get('algorithm')
#     if algorithm == 'KMeans':
#         kmeans = KMeans(n_clusters=3)
#         df['cluster'] = kmeans.fit_predict(df)
#     elif algorithm == 'DBSCAN':
#         dbscan = DBSCAN(eps=0.5, min_samples=5)
#         df['cluster'] = dbscan.fit_predict(df)
#     fig = px.scatter(df, x=df.columns[0], y=df.columns[1], color='cluster')
#     graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
    
#     return render(request, 'data_labeling_app/labeling.html', {'graph_json': graph_json, 'filename': filename})

def cluster_data(request, filename):
    file_path = os.path.join(settings.UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return render(request, 'data_labeling_app/error.html', {'message': 'File not found.'})
    
    df = pd.read_csv(file_path)
    algorithm = request.POST.get('algorithm')
    if algorithm == 'KMeans':
        kmeans = KMeans(n_clusters=3)
        df['cluster'] = kmeans.fit_predict(df)
    elif algorithm == 'DBSCAN':
        dbscan = DBSCAN(eps=0.5, min_samples=5)
        df['cluster'] = dbscan.fit_predict(df)
    df.to_csv(file_path, index=False)  # Save the clustered data back to the file
    
    # Recreate the scatter plot with clusters
    fig = px.scatter(df, x=df.columns[0], y=df.columns[1], color='cluster')
    graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
    
    return render(request, 'data_labeling_app/labeling.html', {'graph_json': graph_json, 'filename': filename})

def export_data(request, filename):
    file_path = os.path.join(settings.UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return render(request, 'data_labeling_app/error.html', {'message': 'File not found.'})
    
    df = pd.read_csv(file_path)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    df.to_csv(response, index=False)
    return response