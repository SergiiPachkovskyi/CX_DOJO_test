from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .forms import UserLoginForm, UserRegisterForm


def index(request):
    return render(request, template_name='django_app/index.html')


def user_registration(request):
    """
    Function for render registration.html
    :param request: WSGIRequest
    :return: render django_app/registration.html
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вдала реєстрація')
            return redirect('home')
        else:
            messages.error(request, 'Помилка реєстрації')
    else:
        form = UserRegisterForm()
    return render(request, 'django_app/registration.html', {"form": form})


def user_login(request):
    """
    Function for render login.html
    :param request: WSGIRequest
    :return: render django_app/login.html
    """
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Помилка авторизації')
    else:
        form = UserLoginForm()
    return render(request, 'django_app/login.html', {"form": form})


def user_logout(request):
    """
    Function for render login.html
    :param request: WSGIRequest
    :return: redirect('home')
    """
    logout(request)
    return redirect('home')
