from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .forms import UserLoginForm, UserRegisterForm, AddUsersForm


def index(request):
    users = User.objects.order_by('-date_joined')
    if request.method == 'POST':
        form = AddUsersForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd.get('file_xml'))
            print(cd.get('file_csv'))
    else:
        form = AddUsersForm()
    return render(request, template_name='django_app/index.html', context={
        'users': users,
        'form': form,
    })


def user_registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Successful registration')
            return redirect('home')
        else:
            messages.error(request, 'Registration error')
    else:
        form = UserRegisterForm()
    return render(request, 'django_app/registration.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Authorization error')
    else:
        form = UserLoginForm()
    return render(request, 'django_app/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('home')
