from homepage.models import Parking
from django import forms
from account.forms import SignupForm
from django.utils.safestring import mark_safe
#====================================
# forms                         #####
#====================================

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
        
        STATE_CHOICES = (
                    ("AL", "Alabama"),
                    ("AK", "Alaska"),
                    ("AZ", "Arizona"),
                    ("AR", "Arkansas"),
                    ("CA", "California"),
                    ("CO", "Colorado"),
                    ("CT", "Connecticut"),
                    ("DE", "Delaware"),
                    ("DC", "District Of Columbia"),
                    ("FL", "Florida"),
                    ("GA", "Georgia"),
                    ("HI", "Hawaii"),
                    ("ID", "Idaho"),
                    ("IL", "Illinois"),
                    ("IN", "Indiana"),
                    ("IA", "Iowa"),
                    ("KS", "Kansas"),
                    ("KY", "Kentucky"),
                    ("LA", "Louisiana"),
                    ("ME", "Maine"),
                    ("MD", "Maryland"),
                    ("MA", "Massachusetts"),
                    ("MI", "Michigan"),
                    ("MN", "Minnesota"),
                    ("MS", "Mississippi"),
                    ("MO", "Missouri"),
                    ("MT", "Montana"),
                    ("NE", "Nebraska"),
                    ("NV", "Nevada"),
                    ("NH", "New Hampshire"),
                    ("NJ", "New Jersey"),
                    ("NM", "New Mexico"),
                    ("NY", "New York"),
                    ("NC", "North Carolina"),
                    ("ND", "North Dakota"),
                    ("OH", "Ohio"),
                    ("OK", "Oklahoma"),
                    ("OR", "Oregon"),
                    ("PA", "Pennsylvania"),
                    ("RI", "Rhode Island"),
                    ("SC", "South Carolina"),
                    ("SD", "South Dakota"),
                    ("TN", "Tennessee"),
                    ("TX", "Texas"),
                    ("UT", "Utah"),
                    ("VT", "Vermont"),
                    ("VA", "Virginia"),
                    ("WA", "Washington"),
                    ("WV", "West Virginia"),
                    ("WI", "Wisconsin"),
                    ("WY", "Wyoming"),)
        self.fields["state"] = forms.ChoiceField(choices=STATE_CHOICES,initial="WA",label='State')
        
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
    CHOICES = (
        (0, '12:00 AM'),
        (1, '1:00 AM'),
        (2, '2:00 AM'),
        (3, '3:00 AM'),
        (4, '4:00 AM'),
        (5, '5:00 AM'),
        (6, '6:00 AM'),
        (7, '7:00 AM'),
        (8, '8:00 AM'),
        (9, '9:00 AM'),
        (10, '10:00 AM'),
        (11, '11:00 AM'),
        (12, '12:00 PM'),
        (13, '1:00 PM'),
        (14, '2:00 PM'),
        (15, '3:00 PM'),
        (16, '4:00 PM'),
        (17, '5:00 PM'),
        (18, '6:00 PM'),
        (19, '7:00 PM'),
        (20, '8:00 PM'),
        (21, '9:00 PM'),
        (22, '10:00 PM'),
        (23, '11:00 PM'),
    )

    fromtime = forms.ChoiceField(choices=CHOICES, required=True, initial=9)
    totime=forms.ChoiceField(choices=CHOICES, required=True, initial=16)
    totalspaces=forms.IntegerField(max_value=20, min_value=1, initial=1)
    CHOICES_Fees = (        
        (1, '1.00 $'),
        (2, '2.00 $'),
        (3, '3.00 $'),
        (4, '4.00 $'),
        (5, '5.00 $'),
        (6, '6.00 $'),
        (7, '7.00 $'),
        (8, '8.00 $'),
        (9, '9.00 $'),
        (10, '10.00 $'),
    )
    fee=forms.ChoiceField(choices=CHOICES_Fees, required=True, initial=3)
    def __init__(self, *args, **kwargs):
        super(ParkingSubForm, self).__init__(*args, **kwargs)
        for f in ['fromtime','totime','totalspaces','fee']:self.fields[f].widget.attrs['class'] = 'form-control'

    def clean_totime(self):
        data = self.cleaned_data['totime']
        if int(self.cleaned_data["totime"]) <= int(self.cleaned_data["fromtime"]): 
            raise forms.ValidationError("Parking End time must be greater than start time.")
        return data   

    
