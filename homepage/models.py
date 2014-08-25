from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils.safestring import mark_safe
from datetime import date

class Parking(models.Model):
    user = models.ForeignKey(User)	
    pic = models.ImageField("Parking Photos", upload_to="images/")    
    streetaddress=models.CharField(max_length=200)
    lat=models.CharField(max_length=20)
    lng=models.CharField(max_length=20)
    totalspaces=models.IntegerField(max_length=3)    
    fromtime=models.DateTimeField()
    totime=models.DateTimeField()    
    upload_date=models.DateTimeField(auto_now_add =True)
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
    class Meta:
        model=Parking
        exclude=['user','totalspaces','fromtime','totime']        
        widgets={'lat': forms.HiddenInput(),'lng': forms.HiddenInput()}