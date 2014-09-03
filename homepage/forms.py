from homepage.models import Parking
from django import forms
from account.forms import SignupForm
#====================================
# forms                         #####
#====================================

class CustSignupForm(SignupForm):
    def clean_licenseplate(self):
        data = self.cleaned_data['licenseplate']
        if self.cleaned_data["is_owner"]=='0' and not data: 
            raise forms.ValidationError("Please Enter license Plate Number.")
        return data
        
    def __init__(self, *args, **kwargs):
        super(CustSignupForm, self).__init__(*args, **kwargs)
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
        USER_TYPE_CHOICES = ( ('0', "I'm Driver"),('1', "I'm Owner"),)
        self.fields["is_owner"] = forms.ChoiceField(choices=USER_TYPE_CHOICES,widget=forms.RadioSelect(),initial='0',label='')
        self.fields["licenseplate"] = forms.CharField(label="license Plate Number", max_length=10,required=False)
        
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
    class Meta:
        model=Parking
        exclude=['user','fromtime','totime']        
        widgets={'lat': forms.HiddenInput(),'lng': forms.HiddenInput(),'pic':MyFileUploadField()}