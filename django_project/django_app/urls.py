from django.urls import path

from .views import *

urlpatterns = [
    path('registration/', user_registration, name='registration'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('', index, name='home'),
]
