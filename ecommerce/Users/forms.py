from django import forms
from django.forms import ModelForm
from .models import Account,UserProfile
from django import forms
from django.contrib import messages

class Registrationform(ModelForm):
    password= forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder':'Enter password'
    }))

    password2= forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder':'Confirm password'
    }))
    class Meta:
        model=Account
        fields=['first_name','last_name','email','phone_number','password','password2']


    # to override the class property
    def __init__(self, *args,**kwargs):
        super(Registrationform, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        data = super(Registrationform,self).clean()
        password1 = data.get('password')
        password2 = data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("password does't match! ")
        return data

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class Verifyform(forms.Form):
    code=forms.CharField(max_length=8,required=True,help_text="enter Code")