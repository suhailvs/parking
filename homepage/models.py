from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils.safestring import mark_safe
#from datetime import date
import calendar,time,datetime
from dateutil import relativedelta

TD = datetime.date.today()
TODAY=datetime.datetime(year=TD.year,month=TD.month,day=TD.day) #datetime
class Weeks(models.Model):
    name=models.CharField(max_length=10)
    def __unicode__(self):
        return self.name

class Parking(models.Model):
    user = models.ForeignKey(User)    
    fromtime=models.DateTimeField()
    totime=models.DateTimeField()
    days=models.ManyToManyField(Weeks,help_text=None)
    totalspaces=models.PositiveIntegerField(max_length=3)
    pic = models.ImageField("Parking Photos", upload_to="images/",blank=True)
    lat=models.CharField(max_length=20)
    lng=models.CharField(max_length=20)
    date_added=models.DateTimeField(auto_now_add =True)
    description=models.CharField(max_length=140)
    status=models.BooleanField(default=True)
    streetaddress=models.CharField(max_length=200)

    def hoursBookedOnDate(self,dt):
        # filter orders on date
        order_items=Orders.objects.filter(parking=self,park_date__startswith=dt)
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
        # loop through available weekdays ie: sunday, monday....etc
        for day in self.days.all():
            # make the weekday as a proper datetime object ie: sunday --> Sept-02-2014
            iter_date=TD+relativedelta.relativedelta(weekday=weekdays[day.name])            
            booked_hours=self.hoursBookedOnDate(iter_date)
            #print booked_hours
            
            # loop through the hours listed by owner ie--> 6-8 --> range(6,9) --> [6,7,8]
            for hr in range(self.fromtime.hour,self.totime.hour+1):                
                # get number of vacancies for that hour
                vacants=self.totalspaces - booked_hours.count(hr)                  

                if vacants > 0 :
                    # convert hr to datetime object
                    # datetime.timedelta(seconds=3600) --> 1hour
                    iter_datetime=datetime.datetime(year=iter_date.year,month=iter_date.month,day=iter_date.day)
                    cur_hour= iter_datetime+datetime.timedelta(seconds=3600 * hr)

                    # to milliseconds
                    cur_hour=int(time.mktime(cur_hour.timetuple()))

                    # mark vacancies on heatmap for that hour                    
                    # sample heat map json--> var data={"946705035":4,...}                    
                    heatmap_data[str(cur_hour)]=vacants
                else:
                    print 'Filled spaces for date: %s' %cur_hour

        # sample heat map json--> var data={"946705035":4,...}   
        return heatmap_data


class Orders(models.Model):
    user = models.ForeignKey(User)
    order_date=models.DateTimeField(auto_now_add =True)
    parking=models.ForeignKey(Parking)
    park_date=models.DateTimeField()
    duration=models.PositiveIntegerField(max_length=2,default=1)
    nspace=models.PositiveIntegerField(max_length=3,default=1)
    paid=models.BooleanField(default=False)

#====================================
# forms                         #####
#====================================

class MyFileUploadField(forms.ClearableFileInput):
    def render(self, name, value, attrs=None):
        html = super(MyFileUploadField, self).render(name, value,attrs)
        html+= '''<input id="cropcoords" type="hidden" name="cropcoords" value="">
        <div class="thumbnail" id="previewimage"></div>'''
        return mark_safe(html);
        
class ParkingForm(forms.ModelForm):   
    def __init__(self, *args, **kwargs):
        super(ParkingForm, self).__init__(*args, **kwargs)
        self.fields['days'].help_text = None 
    class Meta:
        model=Parking
        exclude=['user','fromtime','totime']        
        widgets={'lat': forms.HiddenInput(),'lng': forms.HiddenInput(),'pic':MyFileUploadField()}