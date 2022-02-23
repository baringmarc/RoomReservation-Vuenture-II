from django.shortcuts import render

from ConferenceRoomReservation.roomReservation import admin
from .models import Applicant, ConferenceRoom, Reservation
# Create your views here.

def index(request):
    return render(request, 'index.html')

