from .models import *

def checkValid(form1, form2):
    if form1.is_valid() and form2.is_valid():
        reservations = Reservation.objects.all()
    else:
        return False

    for reservation in reservations:
        if reservation.room.id == form1.instance.room.id:
            if reservation.dateOfUse == form1.instance.dateOfUse:
                if reservation.timeslot.morning == True and form2.instance.morning == True:
                    return False
                elif reservation.timeslot.afternoon == True and form2.instance.afternoon == True:
                    return False
                elif reservation.timeslot.evening == True and form2.instance.evening == True:
                    return False

    return True
