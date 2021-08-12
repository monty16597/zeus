from . import forms

from datetime import datetime, timezone

from django.template import loader
from django.views.generic import ListView
from django.http.response import HttpResponse

from django.contrib.auth.decorators import login_required

from .models import KubernetesAgentConfigModel
from .utils import (describe_resources, describe_resources_url, generate_token, get_namespaces, get_resources, get_datetime_string, get_token, refresh_token)

@login_required
def index(request):
    if request.method == 'POST':
        form = forms.KubernetesAgentConfigForm(request.POST)
        if form.is_valid():
            form.save()
    form = forms.KubernetesAgentConfigForm()
    configs = KubernetesAgentConfigModel.objects.all()
    template = loader.get_template('kubernetes/index.html')
    context = {'page': "kubernetes", 'form': form, "configs": configs}
    return HttpResponse(template.render(context, request))

@login_required
def connect(request, cluster_name):
    cluster = KubernetesAgentConfigModel.objects.get(cluster_name = cluster_name)
    get_token(request, cluster_name)

    # Fetching Details
    data = {
        "ns_count": 0,
        "pd_count": 0,
        "svc_count": 0,
        "pvc_count": 0,
        "ingress_count": 0,
        "namespaces_list": [],
        "pods_list": [],
        "svc_list": [],
        "pvc_list": [],
        "ingress_list": []
    }

    namespaces = get_namespaces(cluster.agent_url, request.session['k8s_token'])
    if namespaces.status_code == 403:
        refresh_token(request, cluster_name)
        namespaces = get_namespaces(cluster.agent_url, request.session['k8s_token'])

    # Fetching data for namespaces
    namespaces = namespaces.json()
    data["namespaces_list"] = namespaces.get("data")
    data["ns_count"] = len(namespaces.get("data"))

    # Fetching data for pods
    pods = get_resources(cluster.agent_url, request.session['k8s_token'], "pods")
    data["pods_list"] = pods.get("data")

    for pod in data["pods_list"]:
        uptime = datetime.utcnow().replace(tzinfo=timezone.utc) - datetime.strptime(pod["start_time"], "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=timezone.utc)
        delta = get_datetime_string(uptime)
        pod["start_time"] = delta
    data["pd_count"] = len(pods.get("data"))

    # Fetching data for svc
    svc = get_resources(cluster.agent_url, request.session['k8s_token'], "svc")
    data["svc_list"] = svc.get("data")
    data["svc_count"] = len(svc.get("data"))

    # Fetching data for pvc
    pvc = get_resources(cluster.agent_url, request.session['k8s_token'], "pvc")
    data["pvc_list"] = pvc.get("data")
    data["pvc_count"] = len(pvc.get("data"))

    # Fetching data for ingress
    ingress = get_resources(cluster.agent_url, request.session['k8s_token'], "ingress")
    data["ingress_list"] = ingress.get("data")
    data["ingress_count"] = len(ingress.get("data"))

    template = loader.get_template('kubernetes/connect.html')
    context = {'page': "kubernetes", "data": data, "cluster_name": cluster_name}
    return HttpResponse(template.render(context, request))

@login_required
def delete(request, cluster_name):
    delete_item = KubernetesAgentConfigModel.objects.filter(cluster_name = cluster_name)
    delete_item.delete()
    form = forms.KubernetesAgentConfigForm()
    configs = KubernetesAgentConfigModel.objects.all()
    template = loader.get_template('kubernetes/index.html')
    context = {'page': "kubernetes", 'form': form, "configs": configs}
    return HttpResponse(template.render(context, request))


# Pod Operations
def describe_pods(request, cluster_name, namespace, pod_name):
    get_token(request, cluster_name)
    print("Returning the dataaaa")
    
    cluster = KubernetesAgentConfigModel.objects.get(cluster_name = cluster_name)
    desc = describe_resources(
        cluster.agent_url, request.session['k8s_token'], namespace, "pod", pod_name
    )
    if desc.status_code == 403:
        refresh_token(request, cluster_name)
        desc = describe_resources(
            cluster.agent_url, request.session['k8s_token'], namespace, "pod", pod_name
        )
    desc = desc.json().get("data")
    return HttpResponse(desc)


class ConfigListView(ListView):
    model = KubernetesAgentConfigModel
    template_name = "kubernetes/config_list.html"
