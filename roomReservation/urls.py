from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index-view'),
    path('login/', LoginView.as_view(), name='login-view'),
    path('contactUs/', ContactUsView.as_view(), name='contactUs-view'),
    path('aboutUs/', AboutUsView.as_view(), name='aboutUs-view'),
    path('rooms/', RoomsView.as_view(), name='rooms-view'),
    path('reservations/', ReservationsView.as_view(), name='reservations-view'),
]