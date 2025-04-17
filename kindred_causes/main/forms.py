from django import forms
from kindred_causes.widgets import TailwindDateInput, TailwindEmailInput, TailwindInput, TailwindSelect, TailwindTextarea, TailwindRating
from .models import EventReview, Event, Skill
from .choices import EventUrgency

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
        widget=TailwindInput(
            attrs={
            "placeholder": "Enter Location",
            "type": "text",
            "class": "input w-full",
            "required": True,
        })
    )

    urgency = forms.ChoiceField(
        choices=EventUrgency.choices,
        label="Urgency",
        # empty_label="Select Urgency level",
        widget=TailwindSelect(
            attrs={
                "class": "fieldset-legend",
            }
        )
    )
    
    required_skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        label="Required Skills",
        widget=forms.CheckboxSelectMultiple

    )
    
    # date = forms.CharField(
    #     widget=TailwindInput(
    #         attrs={
    #             'type': "datetime-local",
    #             'class': "input w-full",
    #             'required': True

    #         }
    #     )
    # )

    date = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],  # Match the datetime-local format
        widget=TailwindInput(
            attrs={
                'type': 'datetime-local',
                'class': 'input w-full',
                'required': True,
            }
        )
    )