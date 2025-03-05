from django import forms
from main.widgets import TailwindDateInput, TailwindEmailInput, TailwindInput, TailwindSelect, TailwindTextarea, TailwindRating, TailwindPassword
from django.contrib.auth.forms import AuthenticationForm, UsernameField



class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=TailwindInput(
        attrs={'placeholder': 'user_name'}))
    
    password = forms.CharField(widget=TailwindPassword(
        attrs={
            'placeholder': 'Password',
        }
    ))