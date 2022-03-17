from django import forms
from .models import ConferenceRoom, Applicant, RoomPrice, Reservation, TimeSlot
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import date

class ApplicantForm(forms.ModelForm):
    firstName = forms.CharField(max_length = 50)
    lastName = forms.CharField(max_length = 50)
    address = forms.CharField(max_length = 150)
    phoneNumber = forms.CharField(max_length = 11)

    class Meta:
        model = Applicant
        fields = ['firstName', 'lastName', 'address', 'phoneNumber']

class ConferenceRoomForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=RoomPrice.objects.all())
    
    class Meta:
        model = ConferenceRoom
        fields = ['name', 'type', 'capacity', 'image']

    # def __init__(self, *args, **kwargs):
    #     super(ConferenceRoomForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].required = True
    #     self.fields['type'].required = True
    #     self.fields['capacity'].required = True

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

class RoomPriceForm(forms.ModelForm):

    class Meta:
        model = RoomPrice
        fields = ['type', 'morning', 'afternoon', 'evening']


class ReservationForm (forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ['room', 'applicant', 'dateOfUse']
        exclude = ['timeslot', 'dateReserved', 'paid', 'completed', 'fee']
        widgets = {
            'dateOfUse': forms.DateInput(attrs={'type': 'date'}),
        } 

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['dateOfUse'].widget.attrs.update({'min': date.today})
        self.fields['dateOfUse'].label = "Date of Use"
        self.fields['room'].label = "Select Room"
        self.fields['applicant'].label = "Select Applicant"

class TimeslotForm (forms.ModelForm):

    class Meta:
        model = TimeSlot
        fields = ['morning', 'afternoon', 'evening']
        exclude = ['id']
       