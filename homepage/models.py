from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils.safestring import mark_safe
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
#widgets = { 'code_postal_immo': MyPostalField(attrs={'style': 'width:300px'}),}   

class addressField(forms.TextInput):
    def render(self, name, value, attrs=None):
        html = super(addressField, self).render(name, value,attrs)
        html+="""
          <p>You can drag and drop the marker to the correct location for precise selection.</p>
	      <div class="form-group">    
	        <div style="height:300px;">
	        <div id="map_canvas" style="width:100%; height:100%"></div>
	        <div id="location" class=""></div>        
	        </div>
	        <!--Latitude:<input type="text" name="lat" class="form-control" id="id_lat">
	        Longitude:<input type="text" name="lng" class="form-control" id="id_lng">
	        <input type="text" id="lbl_longitude">-->           
	      </div>
        """        
        return mark_safe(html);


# Create your models here.
class ParkingForm(forms.ModelForm):    
    class Meta:
        model=Parking
        exclude=['user','totalspaces','fromtime','totime']        
        widgets={'lat': forms.HiddenInput(),'lng': forms.HiddenInput()}