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
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login-view'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html', next_page=None), name='logout-view'),
    path('users/', UsersView.as_view(), name='users-view'),
    path('applicants/', ApplicantsView.as_view(), name='applicants-view'),
    path('prices/', RoomPriceView.as_view(), name='price-view'),
    path('rooms/<int:id>/', RoomLedgerView.as_view(), name='ledger-view'),
]   