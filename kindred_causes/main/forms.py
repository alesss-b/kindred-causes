from django import forms
from django.contrib.auth.models import User
from kindred_causes.widgets import TailwindDateInput, TailwindEmailInput, TailwindInput, TailwindSelect, TailwindTextarea, TailwindRating
from .models import EventReview, Event, Skill, Task, Notification
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


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'capacity', 'location', 'skills']


    name = forms.CharField(
        widget=TailwindInput(
            attrs={
            "title": "Enter Name",
            "placeholder": "Enter Task Name",
            "type": "text",
            "class": "input w-full",
            "maxLength": "100",
            "required": True,
        })
    )

    capacity = forms.IntegerField(
        widget=TailwindInput(
            attrs={
            "title": "Enter Capacity",
            "placeholder": "Enter Task Capacity",
            "type": "number",
            "class": "input w-full",
            "min": "1",
            "required": True,
        })
    )

    description = forms.CharField(
        widget=TailwindTextarea(
            attrs={
            "placeholder": "Enter Task Description",
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


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'admin', 'urgency', 'date']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['admin'].label_from_instance = lambda obj: obj.get_full_name()
        if user is not None:
            self.fields['admin'].initial = user

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

    admin = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name="Admin"),
        label="Event Admin",
        empty_label=None,
        widget=TailwindSelect(
            attrs={
                "class": "fieldset-legend",
                "placeholder": "Choose event admin",
            }
        )
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

class ReadOnlyEventForm(EventForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True

class SkillManagementForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

    name = forms.CharField(
        widget=TailwindInput(
            attrs={
            "title": "Enter Name",
            "placeholder": "Enter Skill Name",
            "type": "text",
            "class": "input w-full",
            "maxLength": "100",
            "required": True,
        })
    )

    description = forms.CharField(
        widget=TailwindTextarea(
            attrs={
            "placeholder": "Enter Skill Description",
            "class": "textarea h-24 text-wrap w-full",
            "required": True,
        })
    )

class NotificationManagementForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['event', 'subject', 'body', 'is_read']
    
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

    subject = forms.CharField(
        widget=TailwindInput(
            attrs={
            "title": "Enter Subject",
            "placeholder": "Enter Subject Name",
            "type": "text",
            "class": "input w-full",
            "maxLength": "100",
            "required": True,
        })
    )

    body = forms.CharField(
        widget=TailwindTextarea(
            attrs={
            "placeholder": "Enter Body",
            "class": "textarea h-24 text-wrap w-full",
            "required": True,
        })
    )

    is_read = forms.BooleanField(
    required=False,  # Important: allows the checkbox to be unchecked
    label="Mark as Read",
    widget=forms.CheckboxInput(
        attrs={
            "class": "checkbox checkbox-success",  # Tailwind classes
        }
    )
)
