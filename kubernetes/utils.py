from kubernetes.models import KubernetesAgentConfigModel
import requests

def get_datetime_string(uptime):
    result = ""
    days = uptime.days
    hours = uptime.seconds//3600
    minutes = (uptime.seconds//60)%60
    if days > 0:
        result = "{0}D {1:.0f}H {2:.0f}M".format(days, hours, minutes)
    elif hours > 0:
        result = "{0:.0f}H {1:.0f}M".format(hours, minutes)
    else:
        result = "{0:.0f}M".format(minutes)
    return result

def get_token_url(agent_url):
    return "{}/token".format(agent_url)

def get_namespace_url(agent_url):
    return "{}/namespaces".format(agent_url)

def get_all_resources_url(agent_url, resource):
    return "{}/all/{}".format(agent_url, resource)

def describe_resources_url(agent_url, namespace, resource, resource_name):
    return "{}/namespace/{}/{}/{}".format(agent_url, namespace, resource, resource_name)

def generate_token(agent_url, username, password):
    data = {"username": username, "password": password, "grant_type": "password"}
    headers = {"Authorization": "Bearer MYREALLYLONGTOKENIGOT"}
    response = requests.post(get_token_url(agent_url), data=data, headers=headers).json()
    return response.get('access_token')

def get_namespaces(agent_url, token):
    headers = {"Authorization": "Bearer {}".format(token)}
    return requests.get(get_namespace_url(agent_url), headers=headers)

def get_resources(agent_url, token, resource):
    headers = {"Authorization": "Bearer {}".format(token)}
    return requests.get(get_all_resources_url(agent_url, resource), headers=headers).json()

def describe_resources(agent_url, token, namespace, resource, resource_name):
    headers = {"Authorization": "Bearer {}".format(token)}
    return requests.get(describe_resources_url(agent_url, namespace, resource, resource_name), headers=headers)


# Util function for view

# Token processing
def get_token(request, cluster_name):
    if not request.session['k8s_token']:
        refresh_token(request, cluster_name)

def refresh_token(request, cluster_name):
    cluster = KubernetesAgentConfigModel.objects.get(cluster_name = cluster_name)
    token = generate_token(cluster.agent_url, cluster.username, cluster.password)
    cluster.token = token
    cluster.save()
    request.session['k8s_token'] = cluster.token