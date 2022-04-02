from django.contrib import admin


from .models import Applicant, ConferenceRoom, Reservation, TimeSlot, RoomPrice

# Register your models here.
admin.site.register(ConferenceRoom)
admin.site.register(Applicant)
admin.site.register(Reservation)
admin.site.register(TimeSlot)
admin.site.register(RoomPrice)