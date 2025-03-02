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