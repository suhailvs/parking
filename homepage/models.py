from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils.safestring import mark_safe
from datetime import date

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
    streetaddress=models.CharField(max_length=200)
    def is_booked(self):
        od=len(Orders.objects.filter(parking=self,order_date__startswith=date.today()))
        return False if od == 0 else True

class Orders(models.Model):
    user = models.ForeignKey(User)
    order_date=models.DateTimeField(auto_now_add =True)
    parking=models.ForeignKey(Parking)
    fromtime=models.TimeField()
    duration=models.IntegerField(max_length=2)
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