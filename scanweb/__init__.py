# __init__.py

from __future__ import absolute_import, unicode_literals

# Hacer que los módulos de Celery se carguen cuando Django se inicie.
from .celery import app as celery_app

__all__ = ('celery_app',)
