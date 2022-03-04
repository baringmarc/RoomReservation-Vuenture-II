from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', IndexView.as_view(), name='index-view'),
    path('contactUs/', ContactUsView.as_view(), name='contactUs-view'),
    path('aboutUs/', AboutUsView.as_view(), name='aboutUs-view'),
    path('rooms/', RoomsView.as_view(), name='rooms-view'),
    path('reservations/', ReservationsView.as_view(), name='reservations-view'),
    path('adminPage/', AdminPageView.as_view(), name='adminPage-view'),
    path('adminReservations/', AdminReservationsView.as_view(), name='adminReservations-view'),
    path('addRoom/', AddRoomView.as_view(), name='addRoom-view'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login-view'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout-view'),
]