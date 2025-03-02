from django.db import models
from django.contrib.auth.models import User
from .choices import EventUrgency

# Base Model:
class Base(models.Model):
    """Abstract base class that adds created_at and updated_at fields to models.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At", db_comment="The date and time the record was created.")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At", db_comment="The date and time the record was last udpated.")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_created_by', blank=True, null=True, verbose_name="Created By", db_comment="The user who created the record.")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_updated_by', blank=True, null=True, verbose_name="Updated By", db_comment="The user who last updated the record.")

    class Meta:
        abstract = True




# Models:
class Skill(Base):
    """ A skill that is required at an Event and that a Volunteer can have.
    """
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Name", db_comment="The name of the Skill.")
    description = models.CharField(null=False, blank=False, verbose_name="Description", db_comment="A detailed description of the Skill.")
    def __str__(self):
        return self.name



class Event(Base):
    """ An Event.
    """
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Name", db_comment="The name of the Event.")
    description = models.CharField(null=False, blank=False, verbose_name="Description", db_comment="A detailed description of the Event.")
    location = models.CharField(null=False, blank=False, verbose_name="Location", db_comment="The location of the event.")
    urgency = models.IntegerField(null=False, blank=False, default=EventUrgency.MEDIUM, choices=EventUrgency.choices, verbose_name="Urgency", db_comment="The urgency of the event.")
    date = models.DateTimeField(null=True, blank=True, verbose_name="Date", db_comment="The date and time of the Event.")
    required_skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.name
    

