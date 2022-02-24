from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index-view'),
    path('login/', LoginView.as_view(), name='login-view'),
]