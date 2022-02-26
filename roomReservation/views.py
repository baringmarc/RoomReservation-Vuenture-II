from django.shortcuts import render
from django.views.generic import View
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