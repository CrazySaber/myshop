import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webshop.settings')

app = Celery('webshop')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()