from django.db import models
from django.utils.safestring import mark_safe
import calendar,time,datetime,os,json
from dateutil import relativedelta,parser
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


WEEKDAY_DICT={'sunday':calendar.SUNDAY,'monday':calendar.MONDAY,
            'tuesday':calendar.TUESDAY,'wednesday':calendar.WEDNESDAY,'thursday':calendar.THURSDAY,
            'friday':calendar.FRIDAY,'saturday':calendar.SATURDAY}

class Weeks(models.Model):
    name=models.CharField(max_length=10)
    def __unicode__(self):
        return self.name

class Parking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    days=models.ManyToManyField(Weeks,help_text=None)  

    fromtime=models.PositiveIntegerField()
    totime=models.PositiveIntegerField()    
    totalspaces=models.PositiveIntegerField()
    fee=models.PositiveIntegerField(help_text="Parking Fee per hour")

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

    def AvailableDays(self):
        TD = datetime.date.today()
        datas=[]#["9-5-2011","14-5-2011","15-5-2011"]
        for day in self.days.all():
            wk1=TD+relativedelta.relativedelta(weekday=WEEKDAY_DICT[day.name])
            wk2=wk1+relativedelta.relativedelta(weeks=+1)
            for dt in [wk1,wk2]:datas.append('{0}-{1}-{2}'.format(dt.day,dt.month,dt.year))
        return datas

    def hoursAvailableOnDate(self,dt):
        #conver dt to proper datestamp
        clean_dt=parser.parse(dt).date()
        TD = datetime.date.today()
        TODAY_TS =datetime.datetime.today()
        datas=[]
        for i in range(2):# 2 weeks
            for day in self.days.all():
                # make the weekday as a proper datetime object ie: sunday --> Sept-02-2014
                ts= TD+relativedelta.relativedelta(weekday=WEEKDAY_DICT[day.name])            
                
                if i==1:
                    #week2
                    ts+=relativedelta.relativedelta(weeks=+1)
                if clean_dt == ts:
                    booked_hours=self.hoursBookedOnDate(clean_dt)
                    # print relativedelta.relativedelta(weekday=WEEKDAY_DICT[day.name]).day
                    # loop through the hours listed by owner ie--> 6-8 --> range(6,9) --> [6,7,8]
                    for hr in range(self.fromtime,self.totime+1):  

                        vacants=self.totalspaces - booked_hours.count(hr)
                        if vacants > 0 :
                            #if today
                            if ts==TD:
                                if TODAY_TS.hour < hr:
                                    # only add available hour if server time hour is smaller than current hour
                                    datas.append(hr)
                            else:
                                # append hours available
                                datas.append(hr)

                    # the weekday is not repeated, so break here
                    break
        return datas if datas else False

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date=models.DateTimeField(auto_now_add =True)
    parking=models.ForeignKey(Parking, on_delete=models.CASCADE)
    park_date=models.DateTimeField()
    duration=models.PositiveIntegerField(default=1)    
    paid=models.BooleanField(default=False)
    invoiceid=models.CharField(max_length=100,blank=True)
    def is_expired(self):
        diff=datetime.datetime.today()- self.order_date  
        # 7minutes -> 420 seconds
        #print 'Server Time:{0} - OrderTime:{1} - Difference:{2} - seconds {3}'.format(datetime.datetime.today(),self.order_date,diff,diff.seconds)
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

