from __future__ import absolute_import
import os,datetime
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

#if settings.site_branch == 'local':broker='django://'
broker='redis://127.0.0.1:31127/0'
#broker='django://'
app = Celery('parking_tasks',broker=broker)

app.config_from_object('django.conf:settings')
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from payments.models import Log_errors
from customemails.views import send_html_email
@app.task
def set_log(pk):
	Log_errors(errors='celery test').save()

@app.task
def send_session_emails(flag,order):
	ctx=dict(order=order,
		deact=order.park_date + datetime.timedelta(0,60*60*order.duration))
	if flag=='ACT':templ='session_active'
	else:
		templ='session_deactive'
	send_html_email(
			template_name=templ,
			params=ctx,
			subj="FLEXTLOT - PARKING SESSION WILL BE {0}IVATED IN 15 MINUTES".format(flag),
			to=[order.user.email])
"""
USAGE:
======
from mysite.celery import set_log
result = set_log.apply_async((1,), countdown=int(request.GET['ts']))
"""

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from homepage.models import Order
# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*",minute=0)))
def remove_inactive_parkingorders():
    m='remove inactive parking cron run at:{}'.format(datetime.datetime.now())
    Log_errors(errors=m).save()
    orders=Order.objects.all()
    for od in orders:        
        if od.is_expired():od.delete()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
