from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .validators import validate_file_xml, validate_file_csv


class UserLoginForm(AuthenticationForm):
    """A class to represent a Login form."""
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))


class UserRegisterForm(UserCreationForm):
    """A class to represent a Register form."""
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': "form-control"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Password confirm",
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AddUsersForm(forms.Form):
    file_csv = forms.FileField(label='file CSV', allow_empty_file=False, validators=[validate_file_csv],
                               widget=forms.FileInput(attrs={'class': "form-control"}))
    file_xml = forms.FileField(label='file XML', allow_empty_file=False, validators=[validate_file_xml],
                               widget=forms.FileInput(attrs={'class': "form-control"}))
