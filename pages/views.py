from django.http import request
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

# class HomePageView(request):
@login_required
def home_page_view(request):
    template_name = 'pages/home.html'
    return render(request, template_name=template_name)

@login_required
def about_page_view(request):
    template_name = 'pages/about.html'
    return render(request, template_name=template_name)