from celery import task
from customemails.views import send_html_email
import os,datetime
@task()
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
