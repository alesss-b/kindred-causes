from django.db import models
from django.contrib.auth.models import User
from .choices import EventUrgency

# Base Model:
class Base(models.Model):
    """Abstract base class that adds created_at and updated_at fields to models.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At", help_text="The date and time the record was created.")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At", help_text="The date and time the record was last udpated.")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_created_by', blank=True, null=True, verbose_name="Created By", help_text="The user who created the record.")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_updated_by', blank=True, null=True, verbose_name="Updated By", help_text="The user who last updated the record.")

    class Meta:
        abstract = True


# Models:
class Skill(Base):
    """ A skill that is required at an Event and that a Volunteer can have.
    """
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Name", help_text="The name of the Skill.")
    description = models.CharField(max_length=254, null=False, blank=False, verbose_name="Description", help_text="A detailed description of the Skill.")
    def __str__(self):
        return self.name


class Event(Base):
    """ An Event.
    """
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Name", help_text="The name of the Event.")
    description = models.CharField(max_length=254,null=False, blank=False, verbose_name="Description", help_text="A detailed description of the Event.")
    location = models.CharField(max_length=254,null=False, blank=False, verbose_name="Location", help_text="The location of the event.")
    urgency = models.IntegerField(null=False, blank=False, default=EventUrgency.MEDIUM, choices=EventUrgency.choices, verbose_name="Urgency", help_text="The urgency of the event.")
    date = models.DateTimeField(null=True, blank=True, verbose_name="Date", help_text="The date and time of the Event.")
    required_skills = models.ManyToManyField(Skill)

    def __str__(self):
        return "{}: {}".format(self.name, self.description)
    

class Task(Base):
    """ A Task to be performed by Volunteers at an Event.
    """
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name="tasks", verbose_name="Related Event", help_text="The parent Event record this task is for.")
    name = models.CharField(max_length=254, null=False, blank=False, verbose_name="Name", help_text="The name of the task.")
    description = models.CharField(max_length=254, null=False, blank=False, verbose_name="Description", help_text="The description of the task.")
    capacity = models.IntegerField(null=False, blank=False, default=-1, verbose_name="Capacity", help_text="The maximum number of Volunteers the Task can hold.")
    location = models.CharField(max_length=254,null=False, blank=True, verbose_name="Location", help_text="The location of the task.")

    def __str__(self):
        return self.name
    

class Notification(Base):
    """ A notification to be sent to users.
    """
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name="notifications", verbose_name="Related Event", help_text="The parent Event record this notification is for.")
    # type = models.CharField(max_length=254, null=False, blank=False, verbose_name="Name", help_text="The name of the task.")
    subject = models.CharField(max_length=254, null=False, blank=False, verbose_name="Subject", help_text="The subject of the message.")
    body = models.CharField(max_length=254,null=False, blank=True, verbose_name="Body", help_text="The content of the message.")

    def __str__(self):
        return self.subject + " " + self.body
    

class Rating(Base):
    """ Base class for rating models
    """
    rating = models.IntegerField(null=False, blank=False, choices=[(i,i) for i in range(5)], verbose_name="Urgency", help_text="The rating out of 5.")
    comments = models.CharField(max_length=254,null=False, blank=True, verbose_name="Comments", help_text="Comments about the rating.")

    class Meta:
        abstract = True


class AttendeeRating(Rating):
    """ A rating of an Event Attendee by an Event Administrator.
    """
    attendee = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="attendee_ratings", verbose_name="Related Attendee", help_text="The attendee this rating is rating.")
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name="attendee_ratings", verbose_name="Related Event", help_text="The event the attendee atteneded to recieve this rating.")


class EventRating(Rating):
    """ A rating of an Event by an Event Attendee.
    """
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name="event_ratings", verbose_name="Related Event", help_text="The event the attendee atteneded to recieve this rating.")
