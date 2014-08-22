from django.db import models
from django.contrib.auth.models import User
from django import forms
class Parking(models.Model):
    user = models.ForeignKey(User)	
    streetaddress=models.CharField(max_length=200,help_text="Street Address or City.")
    lat=models.CharField(max_length=20)
    lng=models.CharField(max_length=20)

# Create your models here.
class ParkingForm(forms.ModelForm):    
    class Meta:
        model=Parking
        exclude=['user']        
        widgets={'lat': forms.HiddenInput(),'lng': forms.HiddenInput(),}