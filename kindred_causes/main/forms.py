from django import forms
from .widgets import TailwindDateInput, TailwindEmailInput, TailwindInput, TailwindSelect, TailwindTextarea, TailwindRating
from .models import EventReview, Event


class EventReviewForm(forms.ModelForm):
    class Meta:
        model = EventReview
        fields = ['event', 'rating', 'comments']

    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        label="Event",
        empty_label=None,
        widget=TailwindSelect(
            attrs={
                "placeholder": "Choose related Event",
            }
        )
    )

    rating = forms.IntegerField(
        widget=TailwindRating()
    )

    comments = forms.CharField(
        widget=TailwindTextarea(
            attrs={
            "placeholder": "Review Comments",
        })
    )

class EventManagementForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'urgency', 'date', 'required_skills']

    name = forms.CharField(
        widget=TailwindInput(
            attrs={
            "title": "Enter Name",
            "placeholder": "Enter Event Name",
            "type": "text",
            "class": "input w-full",
            "maxLength": "100",
            "required": True,
        })
    )

    description = forms.CharField(
        widget=TailwindTextarea(
            attrs={
            "placeholder": "Enter Event Description",
            "class": "textarea h-24 text-wrap w-full",
            "required": True,
        })
    )

    location = forms.CharField(
        widget=TailwindTextarea(
            attrs={
            "placeholder": "Enter Name",
        })
    )

    urgency = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        label="Urgency",
        empty_label=None,
        widget=TailwindSelect(
            attrs={
                "placeholder": "Choose Urgency level of this events",
            }
        )
    )

    required_skills = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        label="Skills",
        empty_label=None,
        widget=TailwindSelect(
            attrs={
                "placeholder": "Choose required skills for this event",
            }
        )
    )