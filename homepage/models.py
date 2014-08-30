from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils.safestring import mark_safe
from datetime import date
import calendar
from dateutil import relativedelta

TODAY = date.today()

class MyFileUploadField(forms.ClearableFileInput):
    def render(self, name, value, attrs=None):
        html = super(MyFileUploadField, self).render(name, value,attrs)
        html+= '''<input id="cropcoords" type="hidden" name="cropcoords" value="">
        <div class="thumbnail" id="previewimage"></div>'''
        return mark_safe(html);
        
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
    streetaddress=models.CharField(max_length=200)
    status=models.BooleanField(default=True)

    def weekAvailability(self):
        """ return data for heat map """
        weekdays={'sunday':calendar.SUNDAY,'monday':calendar.MONDAY,
            'tuesday':calendar.TUESDAY,'wednesday':calendar.WEDNESDAY,'thrusday':calendar.THRUSDAY,
            'friday':calendar.FRIDAY,'saturday':calendar.SATURDAY}
        ods=Orders.objects.filter(parking=self,park_date__gte=TODAY)

        # loop through available weekdays ie: sunday, monday....etc
        for day in self.days.all():
            # make the weekday as a proper datetime object ie: sunday --> Sept-02-2014
            iter_date=TODAY+relativedelta(weekday=weekdays[day.name])
            # filter orders on current weekday
            iter_order=ods.filter(park_date__startswith=iter_date)

            # iter_order[0].park_timings --> '2,3,4'
            # >>> x=['2,3,4','5,6,7','3,4,5']
            # >>> [h for i in x for h in i.split(',') ]
            # ['2', '3', '4', '5', '6', '7', '3', '4', '5']
            booked_hours=[h for p in iter_order for h in p.park_timings.split(',')]

            # loop through the hours listed by owner ie--> [6,7,8,..]
            for hr in range(self.fromtime.hour+1,self.totime.hour+1):
                # check number of vacancies for that hour
                vacants=self.totalspaces - booked_hours.count(str(hr))
                if vacants > 0 :
                    # mark vacancies on heatmap for that hour
                    {'time':iter_date+hr,'vacants':self.totalspaces}
                else:
                    print 'no vacants'




class parkTimings(models.Model):
    ts=models.IntegerField(max_length=2)
    def __unicode__(self):
        return self.ts

class Orders(models.Model):
    user = models.ForeignKey(User)
    order_date=models.DateTimeField(auto_now_add =True)
    parking=models.ForeignKey(Parking)
    park_date=models.DateTimeField()
    park_timings=models.CharField(max_length=200)# comaseperated ordered_hours field
    nspace=models.PositiveIntegerField(max_length=3,default=1)
    paid=models.BooleanField(default=False)
    
# Create your models here.
class ParkingForm(forms.ModelForm):   
    def __init__(self, *args, **kwargs):
        super(ParkingForm, self).__init__(*args, **kwargs)
        self.fields['days'].help_text = None 
    class Meta:
        model=Parking
        exclude=['user','fromtime','totime']        
        widgets={'lat': forms.HiddenInput(),'lng': forms.HiddenInput(),'pic':MyFileUploadField()}