from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, widgets
from kubernetes.models import KubernetesAgentConfigModel

class KubernetesAgentConfigForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(KubernetesAgentConfigForm, self).__init__(*args, **kwargs)

        self.fields['cluster_name'].widget.attrs['placeholder'] = "Cluster Name"
        self.fields['agent_url'].widget.attrs['placeholder'] = "Agent URL"
        self.fields['username'].widget.attrs['placeholder'] = "Username"
        self.fields['password'].widget.attrs['placeholder'] = "Password"

    class Meta:
        model  = KubernetesAgentConfigModel
        fields = ['cluster_name', 'agent_url', 'username', 'password']
        labels = {}
        for field in fields:
            labels.update({field: ''})

        error_messages = {
            'cluster_name': {
                'max_length': "This writer's name is too long.",
            },
        }
