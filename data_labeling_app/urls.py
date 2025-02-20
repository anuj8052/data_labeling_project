from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('label/<str:filename>/', views.label_data, name='label_data'),
    path('cluster/<str:filename>/', views.cluster_data, name='cluster_data'),
    path('export/<str:filename>/', views.export_data, name='export_data'),
]