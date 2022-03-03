from django import forms
from .models import ConferenceRoom


class ConferenceRoomForm(forms.ModelForm):
    class Meta:
        model = ConferenceRoom
        fields = ['name', 'type', 'capacity','morningFee', 'afternoonFee', 'eveningFee']

        