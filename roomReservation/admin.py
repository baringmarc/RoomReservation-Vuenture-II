from django.contrib import admin

from .models import Applicant, ConferenceRoom, Reservation

# Register your models here.
admin.site.register(ConferenceRoom)
admin.site.register(Applicant)
admin.site.register(Reservation)