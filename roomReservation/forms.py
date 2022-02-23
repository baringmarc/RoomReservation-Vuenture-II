from django import forms

class addApplicant(forms.Form):
    name = forms.CharField(max_length = 30, null=True, blank=True)
    address = forms.CharField(max_length = 30, null=True, blank=True)
    phoneNumber = forms.CharField(max_length = 50, null=True, blank=True)