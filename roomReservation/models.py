from django.db import models

# Create your models here.
class ConferenceRoom(models.Model):
    name = models.CharField(max_length = 30, null=True, blank=True)
    type = models.CharField(max_length = 30, null=True, blank=True)
    # timeSlot =

class Applicant(models.Model):
    name = models.CharField(max_length = 50, null=True, blank=True)
    address = models.CharField(max_length = 50, null=True, blank=True)
    phoneNumber = models.CharField(max_length = 10, null=True, blank=True)

class Reservation(models.Model):
    conferenceRoom = models.ForeignKey(ConferenceRoom, on_delete = models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete = models.CASCADE)
    date = models.DateField(null=True, blank=True)