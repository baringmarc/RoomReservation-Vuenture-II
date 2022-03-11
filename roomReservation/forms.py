from django import forms
from .models import ConferenceRoom, Applicant
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ApplicantForm(forms.ModelForm):
    firstName = forms.CharField(max_length = 50)
    lastName = forms.CharField(max_length = 50)
    address = forms.CharField(max_length = 150)
    phoneNumber = forms.CharField(max_length = 11)

    class Meta:
        model = Applicant
        fields = ['firstName', 'lastName', 'address', 'phoneNumber']

class ConferenceRoomForm(forms.ModelForm):
    class Meta:
        model = ConferenceRoom
        fields = ['name', 'type', 'capacity','morningFee', 'afternoonFee', 'eveningFee']

    def __init__(self, *args, **kwargs):
        super(ConferenceRoomForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['type'].required = True
        self.fields['capacity'].required = True
        self.fields['morningFee'].required = True
        self.fields['afternoonFee'].required = True
        self.fields['eveningFee'].required = True

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']




        