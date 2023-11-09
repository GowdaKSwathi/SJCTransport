from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from datetime import datetime, timedelta


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transportproject.settings')

app = Celery('transportproject')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')


# Load task modules from all registered Django app configs.
app.conf.beat_schedule = {
    
}

app.autodiscover_tasks()


# task settings
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')