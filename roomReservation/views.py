from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import datetime
from .reserve import *
from django.contrib import messages

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
        form = ReservationForm()
        form2 = TimeslotForm()
        reservations = Reservation.objects.all()

        context = {'reservations': reservations,
            'form': form, 'form2': form2}
        return render(request, 'reservations.html', context)
    
    def post(self, request):

        form = ReservationForm(request.POST)
        form2 = TimeslotForm(request.POST)
        
        if 'deleteBtn' in request.POST:
            reservationID = request.POST.get('reservationID')
            ConferenceRoom.objects.filter(id=reservationID).delete() 
            return redirect('reservations-view')

        elif 'editBtn' in request.POST:
            if checkValid(form, form2):
                if form.is_valid() and form2.is_valid():
                    form2.save()
                    timeslot_id = TimeSlot.objects.latest('id')
                    form.instance.timeslot = timeslot_id
                    form.save()
                    return redirect('reservations-view')

        elif checkValid(form, form2):
            if form.is_valid() and form2.is_valid():
                form2.save()
                timeslot_id = TimeSlot.objects.latest('id')
                form.instance.timeslot = timeslot_id
                form.save()
                return redirect('reservations-view')
        
        else:
            messages.error(request, 'Reservation not approved. Conflict with existing reservation.')
            return redirect('reservations-view')
            


class RoomsView(LoginRequiredMixin, View):
    def get(self, request):
        form = ConferenceRoomForm(request.POST)
        roomPrice = RoomPrice.objects.all()
        conferenceRooms = ConferenceRoom.objects.all()
        
        context = {'form': form, 'type': roomPrice,
                    'rooms': conferenceRooms}
        return render(request, 'rooms.html', context)
    
    def post(self, request):
        if 'deleteBtn' in request.POST:
            roomid = request.POST.get('roomID')
            ConferenceRoom.objects.filter(id=roomid).delete() 
            return redirect('rooms-view')
        
        elif 'editBtn' in request.POST:
            roomid = request.POST.get('roomID')
            room_name = request.POST.get('roomName')
            room_type = request.POST.get('roomType')
            room_capacity = request.POST.get('roomCapacity')

            ConferenceRoom.objects.filter(id=roomid).update(
                name = room_name, type = room_type, 
                capacity = room_capacity) 
            return redirect('rooms-view')

        else:
            form = ConferenceRoomForm(request.POST) 
            if form.is_valid():
                form.save()
                return redirect('rooms-view')
        
        return render(request, 'rooms.html', {'form': form})

class UsersView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserRegistrationForm()
        user = User.objects.all()
        return render(request, 'users.html', { 'users': user, 'form': form } )
    
    def post(self, request):

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

        elif 'btnUpdate' in request.POST:
            user_id = request.POST.get('userId')
            superuser_status = request.POST.get('isSuperUser')
            staff_status = request.POST.get('staffStatus')
            active_status = request.POST.get('isActive')

            User.objects.filter(id = user_id).update(
                    is_superuser = superuser_status, is_staff = staff_status, 
                    is_active = active_status)
        
        elif 'btnDelete' in request.POST:
            user_id = request.POST.get('userId')
            User.objects.filter(id = user_id).delete()

        return redirect('users-view')

class ApplicantsView(LoginRequiredMixin, View):
    def get(self, request):
        form = ApplicantForm()
        applicant = Applicant.objects.all()
        return render(request, 'applicants.html', { 'applicants': applicant, 'form': form } )
    
    def post(self, request):

        form = ApplicantForm(request.POST)

        if 'btnUpdate' in request.POST:
            applicant_id = request.POST.get('applicantId')
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            address = request.POST.get('address')
            phone_number = request.POST.get('phoneNumber')

            Applicant.objects.filter(id = applicant_id).update(
                    firstName = first_name, lastName = last_name, 
                    address = address, phoneNumber = phone_number)
        
        elif 'btnDelete' in request.POST:
            applicant_id = request.POST.get('applicantId')
            Applicant.objects.filter(id = applicant_id).delete()

        elif form.is_valid():
            form.save()
        return redirect('applicants-view')

class RoomPriceView(LoginRequiredMixin, View):
    def get(self, request):
        form = RoomPriceForm()
        roomPrice = RoomPrice.objects.all()
        return render(request, 'prices.html', { 'prices': roomPrice, 'form': form } )
    
    def post(self, request):

        form = RoomPriceForm(request.POST)

        if 'btnUpdate' in request.POST:
            price_id = request.POST.get('priceId')
            price_type = request.POST.get('priceType')
            morning = request.POST.get('priceM')
            afternoon = request.POST.get('priceA')
            evening = request.POST.get('priceE')
            
            RoomPrice.objects.filter(id = price_id).update(
                priceType = price_type, priceM = morning,
                priceA = afternoon, priceE = evening)
        
        elif 'btnDelete' in request.POST:
            price_id = request.POST.get('priceId')
            RoomPrice.objects.filter(id = price_id).delete()

        elif form.is_valid():
            form.save()
        return redirect('price-view')
    