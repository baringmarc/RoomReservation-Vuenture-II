from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
    
class RoomPrice(models.Model):
    type = models.CharField(max_length=50, null=True)
    morning = models.FloatField(default=0)
    afternoon = models.FloatField(default=0)
    evening = models.FloatField(default=0)
    
    def __str__(self):
        return self.type

class ConferenceRoom(models.Model):
    name = models.CharField(max_length = 30, null=True)
    type = models.ForeignKey(RoomPrice, on_delete=models.CASCADE, null=True)
    capacity = models.IntegerField(null=True)
    image = models.ImageField(upload_to = 'roomImages/', blank = True, null = True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

    def get_image(self):
        if self.image:
            return f'http://127.0.0.1:8000{self.image.url}'
        else:
            return ''

class Applicant(models.Model):
    firstName = models.CharField(max_length = 50, null=True)
    lastName = models.CharField(max_length = 50, null=True)
    address = models.CharField(max_length = 50, null=True)
    phoneNumber = models.CharField(max_length = 11, null=True)

    def __str__(self):
        return self.firstName + " " + self.lastName

class TimeSlot(models.Model):
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    evening = models.BooleanField(default=False)

    def __str__(self):
        name = ""
        if self.morning == True:
            name += "Morning "
        if self.afternoon == True:
            name += "Afternoon "
        if self.evening == True:
            name += "Evening"
            
        return name

class Reservation(models.Model):
    room = models.ForeignKey(ConferenceRoom, on_delete = models.CASCADE, related_name= "room")
    applicant = models.ForeignKey(Applicant, on_delete = models.CASCADE)
    dateOfUse = models.DateField(null=True)
    dateReserved = models.DateField(default=datetime.date.today())
    paid = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    timeslot = models.ForeignKey(TimeSlot, on_delete = models.CASCADE, null=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return self.room.name + " by "+ self.applicant.firstName + " " + self.applicant.lastName

