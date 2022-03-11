from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

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
    