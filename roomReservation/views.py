from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import datetime
from .reserve import *
from django.contrib import messages
from django.db.models import Count, Max, F

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
        applicants = Applicant.objects.all()
        rooms = ConferenceRoom.objects.all()

        if reservations:
            today = datetime.date.today()
            week = datetime.date.today().isocalendar()[1]
            month = datetime.date.today().month
            
            thisWeek = Reservation.objects.filter(dateOfUse__week = week).count()
            thisDay = Reservation.objects.filter(dateOfUse = today).count()
            thisMonth = Reservation.objects.filter(dateOfUse__month = month).count()

            context = {'reservations': reservations,
                'form': form, 'form2': form2, 'applicants': applicants,
                'rooms': rooms, 'today': today, 'thisWeek' : thisWeek, 'thisDay' : thisDay, 'thisMonth': thisMonth}
        else:
            context = {'reservations': reservations,
                'form': form, 'form2': form2, 'applicants': applicants,
                'rooms': rooms,}
        
        return render(request, 'reservations.html', context)
    
    def post(self, request):

        form = ReservationForm(request.POST)
        form2 = TimeslotForm(request.POST)
        
        if form.is_valid() and form2.is_valid():
            if checkValid(form, form2):

                if not form2.instance.morning and not form2.instance.afternoon and not form2.instance.evening:
                    messages.error(request, 'Reservation not added. Please select at least one timeslot.')
                    return redirect('reservations-view')

                form2.save()
                timeslot_id = TimeSlot.objects.latest('id')
                form.instance.timeslot = timeslot_id
                form.instance.fee = calculateFee_1(form)
                form.save()

                messages.success(request, 'Reservation added.')
                return redirect('reservations-view')
        
        elif 'deleteBtn' in request.POST:
            reservationID = request.POST.get('reservationID')
            timeslotID = request.POST.get('timeslotID')
            Reservation.objects.filter(id=reservationID).delete()
            TimeSlot.objects.filter(id=timeslotID).delete()
            messages.warning(request, 'Reservation canceled.')
            return redirect('reservations-view')

        elif 'payBtn' in request.POST:
            reservationID = request.POST.get('reservationID')
            Reservation.objects.filter(id=reservationID).update(paid="True") 
            messages.success(request, 'Reservation recorded as paid.')
            return redirect('reservations-view')
        
        elif 'editBtn' in request.POST:
            form3 = {'reserveID': request.POST.get('reserveID'),
            'roomID': request.POST.get('reserveRoom'),
            'dateOfUse': request.POST.get('reserveDate'),
            'applicantID': request.POST.get('reserveAppli')}
            form4 = {'timeslotID': request.POST.get('timeslotID'),
            'morning': request.POST.get('morning')=='on', 
            'afternoon': request.POST.get('afternoon')=='on',
            'evening': request.POST.get('evening')=='on'}

            if not form4['morning'] and not form4['afternoon'] and not form4['evening']:
                messages.error(request, 'Please select at least one timeslot.')
                return redirect('reservations-view')
            
            elif checkValidEdit(form3, form4):
                reserveID = form3['reserveID']
                reserveRoom = form3['roomID']
                reserveDate = form3['dateOfUse']
                reserveApplicant = form3['applicantID']

                timeslotID = form4['timeslotID']
                morning_new = form4['morning']
                afternoon_new = form4['afternoon']
                evening_new = form4['evening']
                
                TimeSlot.objects.filter(id=timeslotID).update(
                    morning=morning_new, afternoon=afternoon_new,
                    evening=evening_new)

                fee_new = calculateFee_2(form3, form4)

                Reservation.objects.filter(id=reserveID).update(
                    room=reserveRoom, dateOfUse=reserveDate,
                    applicant=reserveApplicant, fee=fee_new)

                messages.success(request, 'Reservation successfully updated.')


                return redirect('reservations-view')    
    
        messages.error(request, 'Reservation not approved. Conflict with existing reservation.')
        return redirect('reservations-view')
            


class RoomsView(LoginRequiredMixin, View):
    def get(self, request):
        form = ConferenceRoomForm(request.POST)
        roomPrice = RoomPrice.objects.all()
        conferenceRooms = ConferenceRoom.objects.all()

        if conferenceRooms:
            rooms = Reservation.objects.values('room').annotate(booked=Count('room'))
            maxbooked = max(room['booked'] for room in rooms)
            getMaxRooms = rooms.filter(booked=maxbooked)
            maxRoom = getMaxRooms[0]['room']
            mostBookedRoom = ConferenceRoom.objects.get(pk=maxRoom)
            context = {'form': form, 'type': roomPrice, 
            'rooms': conferenceRooms, 'mostBooked': mostBookedRoom,
            'booked':maxbooked}
        else:
            context = {'form': form, 'type': roomPrice, 'rooms': conferenceRooms}
        return render(request, 'rooms.html', context)
    
    def post(self, request):
        if 'deleteBtn' in request.POST:
            roomid = request.POST.get('roomID')
            ConferenceRoom.objects.filter(id=roomid).delete()
            messages.warning(request, 'Room removed.') 
            return redirect('rooms-view')
        
        elif 'editBtn' in request.POST:
            roomid = request.POST.get('roomID')
            room_name = request.POST.get('roomName')
            room_type = request.POST.get('roomType')
            room_capacity = request.POST.get('roomCapacity')
            room_image = request.FILES.get('image')

            print(room_image)
            
            ConferenceRoom.objects.filter(id=roomid).update(
                name = room_name, type = room_type, 
                capacity = room_capacity, image = room_image) 
            messages.success(request, 'Room successfully updated.')
            return redirect('rooms-view')

        else:
            form = ConferenceRoomForm(request.POST, request.FILES) 
            if form.is_valid():
                form.save()
                messages.success(request, 'Room successfully added.')
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
            messages.success(request, 'New User registered successfully.')

        elif 'btnUpdate' in request.POST:
            user_id = request.POST.get('userId')
            superuser_status = request.POST.get('isSuperUser')
            staff_status = request.POST.get('staffStatus')
            active_status = request.POST.get('isActive')

            User.objects.filter(id = user_id).update(
                    is_superuser = superuser_status, is_staff = staff_status, 
                    is_active = active_status)
            messages.success(request, 'User successfully updated.')        
        
        elif 'btnDelete' in request.POST:
            user_id = request.POST.get('userId')
            User.objects.filter(id = user_id).delete()
            messages.warning(request, 'User successfully deleted.')

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
            messages.success(request, 'Applicant successfuly updated.')
        
        elif 'btnDelete' in request.POST:
            applicant_id = request.POST.get('applicantId')
            Applicant.objects.filter(id = applicant_id).delete()
            messages.warning(request, 'Applicant deleted.')

        elif form.is_valid():
            form.save()
            messages.success(request, 'Applicant successfully added.')
        return redirect('applicants-view')

class RoomPriceView(LoginRequiredMixin, View):
    def get(self, request):
        form = RoomPriceForm()
        roomPrice = RoomPrice.objects.all()
        return render(request, 'prices.html', { 'prices': roomPrice, 'form': form } )
    
    def post(self, request):

        form = RoomPriceForm(request.POST)

        if 'btnUpdate' in request.POST:
            price_id = request.POST.get('priceID')
            price_type = request.POST.get('priceType')
            pMorning = request.POST.get('priceM')
            pAfternoon = request.POST.get('priceA')
            pEvening = request.POST.get('priceE')
            
            RoomPrice.objects.filter(id = price_id).update(
                type = price_type, morning = pMorning,
                afternoon = pAfternoon, evening = pEvening)

            messages.success(request, 'Room price type successfully updated.')

        elif 'btnDelete' in request.POST:
            price_id = request.POST.get('priceId')
            RoomPrice.objects.filter(id = price_id).delete()
            messages.warning(request, 'Room price type removed.')

        elif form.is_valid():
            form.save()
            messages.success(request, 'Room price type successfully added.')
        return redirect('price-view')

class RoomLedgerView(View):
    
    def get(self, request, id):
        rID = id
        reservation = Reservation.objects.filter(room__id = rID).all()
        room = ConferenceRoom.objects.get(room = rID)
        context = {'reservation': reservation, 'room': room}
        return render(request, 'roomLedger.html', context)
