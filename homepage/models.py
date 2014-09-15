from django.db import models
from django.utils.safestring import mark_safe
import calendar,time,datetime,os
from dateutil import relativedelta,parser
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()
TD = datetime.date.today()
WEEKDAY_DICT={'sunday':calendar.SUNDAY,'monday':calendar.MONDAY,
            'tuesday':calendar.TUESDAY,'wednesday':calendar.WEDNESDAY,'thursday':calendar.THURSDAY,
            'friday':calendar.FRIDAY,'saturday':calendar.SATURDAY}

class Weeks(models.Model):
    name=models.CharField(max_length=10)
    def __unicode__(self):
        return self.name

class Parking(models.Model):
    user = models.ForeignKey(User)
    days=models.ManyToManyField(Weeks,help_text=None)  

    fromtime=models.PositiveIntegerField(max_length=2)
    totime=models.PositiveIntegerField(max_length=2)    
    totalspaces=models.PositiveIntegerField(max_length=3)
    fee=models.PositiveIntegerField(max_length=5, help_text="Parking Fee per hour")

    pic = models.ImageField("Parking Photos", upload_to="images/",blank=True)
    lat=models.CharField(max_length=20)
    lng=models.CharField(max_length=20)
    date_added=models.DateTimeField(auto_now_add =True)
    description=models.CharField(max_length=140,help_text="Provide name of location or business, and pertinent details (e.g. use unmarked parking space only, use space with sign marked 'Private' located at end of alley, park off pavement, etc.)")
    
    status=models.BooleanField(default=True, help_text="Uncheck to temporarily deactivate listing")
    streetaddress=models.CharField(max_length=200)
    

    def hoursBookedOnDate(self,dt):
        # filter orders on date
        order_items=Order.objects.filter(parking=self,park_date__startswith=dt)
        # >>> for od in o: print od.park_date, od.duration
        # [2014-09-01 07:00:00 2, 2014-09-01 06:00:00 4]
        # park.hoursBookedOnDate(date(2014,9,1)) --> [7, 8, 6, 7, 8, 9]

        return [h for i in order_items for h in range(i.park_date.hour,i.park_date.hour+i.duration)]

    def hoursAvailableOnDate(self,dt):
        #conver dt to proper datestamp
        clean_dt=parser.parse(dt).date()

        datas=[]
        for day in self.days.all():
            # make the weekday as a proper datetime object ie: sunday --> Sept-02-2014
            ts= TD+relativedelta.relativedelta(weekday=WEEKDAY_DICT[day.name])

            if clean_dt == TD+relativedelta.relativedelta(weekday=WEEKDAY_DICT[day.name]):
                booked_hours=self.hoursBookedOnDate(clean_dt)

                # loop through the hours listed by owner ie--> 6-8 --> range(6,9) --> [6,7,8]
                for hr in range(self.fromtime,self.totime+1):  

                    vacants=self.totalspaces - booked_hours.count(hr)
                    if vacants > 0 :
                        # append hours available
                        datas.append(hr)

                # the weekday is not repeated, so break here
                break
        return datas if datas else False

    def get_picurl(self):
        url=None
        if self.pic:
            fname=os.path.join(settings.MEDIA_ROOT, self.pic.name)
            url=fname[:-4]+'_crop.jpg'
        return url

    

class Order(models.Model):
    user = models.ForeignKey(User)
    order_date=models.DateTimeField(auto_now_add =True)
    parking=models.ForeignKey(Parking)
    park_date=models.DateTimeField()
    duration=models.PositiveIntegerField(max_length=2,default=1)
    nspace=models.PositiveIntegerField(max_length=3,default=1)
    paid=models.BooleanField(default=False)
    invoiceid=models.CharField(max_length=100,blank=True)
    def is_expired(self):
        diff=datetime.datetime.today()- self.order_date  
        # 7minutes -> 420 seconds      
        return True if diff.seconds > 420 else False

from django.db.models.signals import pre_delete

def delete_parking_images(sender, instance, using, **kwargs):
    if instance.pic:
        fname=os.path.join(settings.MEDIA_ROOT, instance.pic.name)
        try:
            os.remove(fname[:-4]+'_160.jpg')
            os.remove(fname[:-4]+'_crop.jpg')
        except:
            pass
pre_delete.connect(delete_parking_images, sender=Parking)

