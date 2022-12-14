from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.urls import reverse

from .forms import UserLoginForm, UserRegisterForm, DataCollectionForm
from .utils import load_files
from .models import Profile


def index(request):
    profiles = Profile.objects.filter(user__is_staff=False).order_by('-user__date_joined').select_related('user')

    if request.method == 'POST':
        form = DataCollectionForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            load_files(cd.get('file_csv').file, cd.get('file_xml').file)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = DataCollectionForm()
    return render(request, template_name='django_app/index.html', context={
        'profiles': profiles,
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
