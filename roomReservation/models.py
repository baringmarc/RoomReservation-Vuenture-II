from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class ConferenceRoom(models.Model):
    name = models.CharField(max_length = 30, null=True, blank=True)
    type = models.CharField(max_length = 30, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    morningFee = models.FloatField(null=True, blank=True)
    afternoonFee = models.FloatField(null=True, blank=True)
    eveningFee = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Applicant(models.Model):
    firstName = models.CharField(max_length = 50, null=True, blank=True)
    lastName = models.CharField(max_length = 50, null=True, blank=True)
    address = models.CharField(max_length = 50, null=True, blank=True)
    phoneNumber = models.CharField(max_length = 11, null=True, blank=True)

    def __str__(self):
        return self.firstName + self.lastName

class TimeSlot(models.Model):
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    evening = models.BooleanField(default=False)

    def __str__(self):
        name = ""
        if self.morning == True:
            name += "Morning"
        if self.afternoon == True:
            name += "Afternoon"
        if self.evening == True:
            name += "Evening"
            
        return self.name

class Reservation(models.Model):
    room = models.ForeignKey(ConferenceRoom, on_delete = models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete = models.CASCADE)
    dateOfUse = models.DateField(null=True, blank=True)
    dateReserved = models.DateField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    timeslot = models.ForeignKey(TimeSlot, on_delete = models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.room.name + " by "+ self.applicant.firstName + " " + self.applicant.lastName

