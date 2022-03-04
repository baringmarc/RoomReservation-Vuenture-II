from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('rooms-view')
        else:
            return render(request, 'index.html')

class ContactUsView(View):
    def get(self, request):
        return render(request, 'contactUs.html')

class AboutUsView(View):
    def get(self, request):
        return render(request, 'aboutUs.html')

class ReservationsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'reservations.html')

class RoomsView(LoginRequiredMixin, View):
    def get(self, request):
        form = ConferenceRoomForm(request.POST)
        conferenceRooms = ConferenceRoom.objects.all()
        reservations = Reservation.objects.all()
        context = {'form': form,
                    'rooms': conferenceRooms,
                    'reservations': reservations}
        return render(request, 'rooms.html', context)
    
    def post(self, request):
        if 'deleteBtn' in request.POST:
            roomid = request.POST.get('roomID')
            ConferenceRoom.objects.filter(id=roomid).delete() 
            print('Room deleted')
            return redirect('rooms-view')
        
        elif 'editBtn' in request.POST:
            roomId = request.POST.get('roomID')
            roomName = request.POST.get('roomName')
            roomType = request.POST.get('roomType')
            roomCapa = request.POST.get('roomCapacity')
            roomMFee = request.POST.get('roomMFee')
            roomAFee = request.POST.get('roomAFee')
            roomEFee = request.POST.get('roomEFee')
            
            ConferenceRoom.objects.filter(id = roomId).update(
                name = roomName, type = roomType, capacity = roomCapa,
                morningFee = roomMFee, afternoonFee = roomAFee,
                eveningFee = roomEFee
            )
            return redirect('rooms-view')

        else:
            form = ConferenceRoomForm(request.POST) 
            if form.is_valid():
                form.save()
                return redirect('rooms-view')
        
        return render(request, 'rooms.html', {'form': form})