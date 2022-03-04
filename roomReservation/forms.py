from django import forms
from .models import ConferenceRoom


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



        