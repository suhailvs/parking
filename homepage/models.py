from django.db import models
#from django.contrib.auth.models import User

from django.utils.safestring import mark_safe
#from datetime import date
import calendar,time,datetime
from dateutil import relativedelta
#from payments.models import Order
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    licenseplate = models.CharField(max_length=10, blank=True)
    state=models.CharField(max_length=2)


TD = datetime.date.today()
TODAY=datetime.datetime(year=TD.year,month=TD.month,day=TD.day) #datetime
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
    fee=models.PositiveIntegerField(max_length=5, help_text="$ Parking Fee per hour")

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
        
    def weekAvailability(self):
        """ return data for heat map for a parking"""
        weekdays={'sunday':calendar.SUNDAY,'monday':calendar.MONDAY,
            'tuesday':calendar.TUESDAY,'wednesday':calendar.WEDNESDAY,'thursday':calendar.THURSDAY,
            'friday':calendar.FRIDAY,'saturday':calendar.SATURDAY}
        #iter_order=Orders.objects.filter(parking=self,park_date__gte=TODAY)

        heatmap_data=dict()
        new_data=[] #[{year: 2014, month: 15,day:3,hour:4, value:20},...]

        # loop through available weekdays ie: sunday, monday....etc
        for day in self.days.all():
            # make the weekday as a proper datetime object ie: sunday --> Sept-02-2014
            ts=TD+relativedelta.relativedelta(weekday=weekdays[day.name])            
            booked_hours=self.hoursBookedOnDate(ts)            
            
            # loop through the hours listed by owner ie--> 6-8 --> range(6,9) --> [6,7,8]
            for hr in range(self.fromtime,self.totime+1):                
                # get number of vacancies for that hour
                vacants=self.totalspaces - booked_hours.count(hr)                  

                if vacants > 0 :
                    new_data.append(dict(year=ts.year,month=ts.month,day=ts.day,hour=hr,value=vacants))
                                
        # [{year: 2014, month: 15,day:3,hour:4, value:20},...]
        #print new_data
        return new_data

class Order(models.Model):
    user = models.ForeignKey(User)
    order_date=models.DateTimeField(auto_now_add =True)
    parking=models.ForeignKey(Parking)
    park_date=models.DateTimeField()
    duration=models.PositiveIntegerField(max_length=2,default=1)
    nspace=models.PositiveIntegerField(max_length=3,default=1)
    paid=models.BooleanField(default=False)
    invoiceid=models.CharField(max_length=100,blank=True)