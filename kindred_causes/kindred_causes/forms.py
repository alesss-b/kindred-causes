from django import forms
from .widgets import TailwindDateInput, TailwindEmailInput, TailwindInput, TailwindSelect, TailwindTextarea, TailwindRating, TailwindPassword, TailwindUsername
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm



class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=TailwindUsername(
        attrs={'placeholder': 'Username'}))
    
    password = forms.CharField(widget=TailwindPassword(
        attrs={
            'placeholder': 'Password',
        }
    ))


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=TailwindUsername(
        attrs={'placeholder': 'Username'}))
    
    email = forms.EmailField(
        required=True,
        widget=TailwindEmailInput(attrs={'placeholder': 'Email'}),
    )

    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=TailwindInput(attrs={'placeholder': 'First name'}),
    )

    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=TailwindInput(attrs={'placeholder': 'Last name'}),
    )
    
    password1 = forms.CharField(widget=TailwindPassword(
        attrs={
            'placeholder': 'Password',
            'verbose_name': 'Password'
        }
    ))

    password2 = forms.CharField(widget=TailwindPassword(
        attrs={
            'placeholder': 'Confirm Password',
            'verbose_name': 'Confirm Password'
        }
    ))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        field_classes = {'username': UsernameField}