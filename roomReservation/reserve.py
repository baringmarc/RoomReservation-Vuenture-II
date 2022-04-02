from .models import *

def checkValid(form1, form2):
    if form1.is_valid() and form2.is_valid():
        reservations = Reservation.objects.all()
        for reservation in reservations:
            if reservation.room.id == form1.instance.room.id:
                if reservation.dateOfUse == form1.instance.dateOfUse:
                    if reservation.timeslot.morning == True and form2.instance.morning == True:
                        return False
                    elif reservation.timeslot.afternoon == True and form2.instance.afternoon == True:
                        return False
                    elif reservation.timeslot.evening == True and form2.instance.evening == True:
                        return False
    else:
        return False

    return True

def checkValidEdit(form1, form2):
    if form1['reserveID'] and form1['roomID'] and form1['dateOfUse'] and form2['timeslotID']:

        reservations = Reservation.objects.filter(room__id = form1['roomID']).all()
        
        for reservation in reservations: 
            if not reservation.timeslot.id == form2['timeslotID']:
                if str(reservation.dateOfUse) == str(form1['dateOfUse']):
                    if reservation.timeslot.morning == True and form2['morning'] == True:
                        return False
                    elif reservation.timeslot.afternoon == True and form2['afternoon'] == True:
                        return False
                    elif reservation.timeslot.evening == True and form2['evening'] == True:
                        return False
    else:
        return False

    return True

def calculateFee_1(form):
    fee = 0
    if form.is_valid():
        roomtype = RoomPrice.objects.get(id=form.instance.room.type.id)
        if form.instance.timeslot.morning == True:
            fee += roomtype.morning
        if form.instance.timeslot.afternoon == True:
            fee += roomtype.afternoon
        if form.instance.timeslot.evening == True:
            fee += roomtype.evening

    return fee 

def calculateFee_2(form1, form2):
    fee = 0
    if form1 and form2:
        room = ConferenceRoom.objects.filter(id=form1['roomID']).get()
        roomtype = RoomPrice.objects.filter(id=room.type.id).get()
        if form2['morning'] == True:
            fee += roomtype.morning
        if form2['afternoon'] == True:
            fee += roomtype.afternoon
        if form2['evening'] == True:
            fee += roomtype.evening

    return fee 

        
