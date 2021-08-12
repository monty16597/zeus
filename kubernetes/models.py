from django.db import models

# Create your models here.
class KubernetesAgentConfigModel(models.Model):
    cluster_name = models.CharField(
        max_length=32,
        primary_key=True
    )
    agent_url = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    username = models.CharField(
        max_length=32,
        null=False,
        blank=False
    )
    password = models.CharField(
        max_length=64,
        null=False,
        blank=False
    )
    token = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
