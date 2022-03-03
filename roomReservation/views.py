from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .forms import *
from .models import *

# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

class ContactUsView(View):
    def get(self, request):
        return render(request, 'contactUs.html')

class AboutUsView(View):
    def get(self, request):
        return render(request, 'aboutUs.html')

class RoomsView(View):
    def get(self, request):
        return render(request, 'rooms.html')

class ReservationsView(View):
    def get(self, request):
        return render(request, 'reservations.html')

class AdminReservationsView(View):
    def get(self, request):
        return render(request, 'adminReservations.html')

class AddRoomView(View):
    def get(self, request):
        return render(request, 'addRoom.html')

class AdminPageView(View):
    def get(self, request):
        form = ConferenceRoomForm(request.POST)
        conferenceRooms = ConferenceRoom.objects.all()
        context = {'form': form,
                    'rooms': conferenceRooms}
        return render(request, 'adminPage.html', context)
    
    def post(self, request):
        if 'deleteBtn' in request.POST:
            roomid = request.POST.get('roomID')
            ConferenceRoom.objects.filter(id=roomid).delete() 
            print('Room deleted')
            return redirect('adminPage-view')
        
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
            return redirect('adminPage-view')

        else:
            form = ConferenceRoomForm(request.POST) 
            if form.is_valid():
                form.save()
                return redirect('adminPage-view')
        
        return render(request, 'adminPage.html', {'form': form})