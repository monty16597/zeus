from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='kubernetes.index'),
    path('config', views.ConfigListView.as_view(), name='kubernetes.config'),
    path('connect/<cluster_name>/', views.connect, name='kubernetes.connect'),
    path('delete/<cluster_name>/', views.delete, name='kubernetes.delete'),
    path('describe/<cluster_name>/<namespace>/<pod_name>/', views.describe_pods, name='kubernetes.describe.pods')
]
