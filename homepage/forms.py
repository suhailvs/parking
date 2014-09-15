from homepage.models import Parking
from django import forms
from account.forms import SignupForm
from django.utils.safestring import mark_safe
from homepage.choices import STATE_CHOICES,FEE_CHOICES,TIME_CHOICES
#====================================
# forms                         #####
#====================================
from captcha.fields import ReCaptchaField
class CustSignupForm(SignupForm):
    def clean_licenseplate(self):
        data = self.cleaned_data['licenseplate']
        if self.cleaned_data["is_owner"]=='0' and not data: 
            raise forms.ValidationError("Please Enter license Plate Number.")
        return data

    def clean_password(self):
        #if 'password' in self.cleaned_data and len(self.cleaned_data['password'])<4:
        data = self.cleaned_data['password']
        if len(data)<4:
            raise forms.ValidationError("Password must have minimum 4 characters.")
        return data

    
    def __init__(self, *args, **kwargs):
        super(CustSignupForm, self).__init__(*args, **kwargs)        
        USER_TYPE_CHOICES = ( ('0', "I'm Driver"),('1', "I'm Owner"),)
        self.fields["is_owner"] = forms.ChoiceField(choices=USER_TYPE_CHOICES,widget=forms.RadioSelect(),initial='0',label='')
        self.fields["licenseplate"] = forms.CharField(label="license Plate Number", max_length=10,required=False)
        
        
        self.fields["state"] = forms.ChoiceField(choices=STATE_CHOICES,initial="WA",label='State')
        self.fields["captcha"] = ReCaptchaField()
        
        #current_order = self.fields.keyOrder
        #print current_order
        #self.fields.keyOrder = ["full_name",'email'] + [field for field in current_order if not field in ('full_name','email')]


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
        self.fields['status'].label='Live'
    class Meta:
        model=Parking
        exclude=['user','fromtime','totime','totalspaces','fee']        
        widgets={'lat': forms.HiddenInput(),'lng': forms.HiddenInput(),'pic':MyFileUploadField()}


class ParkingSubForm(forms.Form):   
    #fromtime=forms.IntegerField()
   
    fromtime = forms.ChoiceField(choices=TIME_CHOICES, required=True, initial=9)
    totime=forms.ChoiceField(choices=TIME_CHOICES, required=True, initial=16)
    totalspaces=forms.IntegerField(max_value=20, min_value=1, initial=1)
    
    fee=forms.ChoiceField(choices=FEE_CHOICES, required=True, initial=3)
    def __init__(self, *args, **kwargs):
        super(ParkingSubForm, self).__init__(*args, **kwargs)
        for f in ['fromtime','totime','totalspaces','fee']:self.fields[f].widget.attrs['class'] = 'form-control'

    def clean_totime(self):
        data = self.cleaned_data['totime']
        if int(self.cleaned_data["totime"]) <= int(self.cleaned_data["fromtime"]): 
            raise forms.ValidationError("Parking End time must be greater than start time.")
        return data   

    
