from __future__ import absolute_import
import os,datetime
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

if settings.site_branch == 'local':broker='django://'
else:broker='redis://127.0.0.1:31127/0'
app = Celery('parking_tasks',broker=broker)

app.config_from_object('django.conf:settings')
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from payments.models import Log_errors

@app.task
def set_log(pk):
	Log_errors(errors='celery test').save()

"""
USAGE:
======
from mysite.celery import set_log
result = set_log.apply_async((1,), countdown=int(request.GET['ts']))
"""

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))