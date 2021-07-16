from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='automation.index'),
    path('patch/jenkinsfile', views.patch_jenkinsfile, name='automation.patch.jenkinsfile'),
]
