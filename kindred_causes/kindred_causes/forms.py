from django import forms
from main.widgets import TailwindDateInput, TailwindEmailInput, TailwindInput, TailwindSelect, TailwindTextarea, TailwindRating
from django.contrib.auth.forms import AuthenticationForm, UsernameField



class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=TailwindInput(
        attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=TailwindInput(
        attrs={
            'placeholder': 'Password',
        }
    ))

    comments = forms.CharField(
        widget=TailwindTextarea(
            attrs={
            "placeholder": "Review Comments",
        })
    )