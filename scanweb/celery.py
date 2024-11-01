# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scanweb.settings')

# Crea una instancia de Celery
app = Celery('scanweb')

# Cargar la configuración de Celery desde Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descubrir las tareas definidas en los archivos tasks.py
app.autodiscover_tasks()
