from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kbt_marketplace.settings")

app = Celery("kbt_marketplace")

# Load task modules from all registered Django app configs
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks in Django apps
app.autodiscover_tasks()
