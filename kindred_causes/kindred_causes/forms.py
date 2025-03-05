from django import forms
from .widgets import TailwindDateInput, TailwindEmailInput, TailwindInput, TailwindSelect, TailwindTextarea, TailwindRating, TailwindPassword, TailwindUsername
from django.contrib.auth.forms import AuthenticationForm, UsernameField



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