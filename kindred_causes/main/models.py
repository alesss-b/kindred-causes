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
    admin = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="admin_events", verbose_name="Event Admin", help_text="The admin who is in charge of the Event.")
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Name", help_text="The name of the Event.")
    description = models.CharField(max_length=254,null=False, blank=False, verbose_name="Description", help_text="A detailed description of the Event.")
    location = models.CharField(max_length=254,null=False, blank=False, verbose_name="Location", help_text="The location of the event.")
    urgency = models.IntegerField(null=False, blank=False, default=EventUrgency.MEDIUM, choices=EventUrgency.choices, verbose_name="Urgency", help_text="The urgency of the event.")
    date = models.DateTimeField(null=True, blank=True, verbose_name="Date", help_text="The date and time of the Event.")

    def __str__(self):
        return "{}: {}".format(self.name, self.description)


class Task(Base):
    """ A Task to be performed by Volunteers at an Event.
    """
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name="tasks", verbose_name="Related Event", help_text="The parent Event record this task is for.")
    attendees = models.ManyToManyField(User, blank=True, related_name="tasks")
    name = models.CharField(max_length=254, null=False, blank=False, verbose_name="Name", help_text="The name of the task.")
    description = models.CharField(max_length=254, null=False, blank=False, verbose_name="Description", help_text="The description of the task.")
    capacity = models.IntegerField(null=False, blank=False, default=-1, verbose_name="Capacity", help_text="The maximum number of Volunteers the Task can hold.")
    location = models.CharField(max_length=254,null=False, blank=True, verbose_name="Location", help_text="The location of the task.")
    skills = models.ManyToManyField(Skill, blank=True)

    @property
    def attendee_count(self):
        return self.attendees.count()

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
    

class Review(Base):
    """ Base class for review models
    """
    rating = models.IntegerField(null=False, blank=False, choices=[(i,i) for i in range(1, 6)], verbose_name="Rating", help_text="The rating out of 5.")
    comments = models.CharField(max_length=254,null=False, blank=True, verbose_name="Comments", help_text="Comments about the review.")

    class Meta:
        abstract = True


class AttendeeReview(Review):
    """ A Review of an Event Attendee by an Event Administrator.
    """
    attendee = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="attendee_reviews", verbose_name="Related Attendee", help_text="The attendee this review is reviewing.")
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name="attendee_reviews", verbose_name="Related Event", help_text="The event the attendee atteneded to recieve this reviewing.")


class EventReview(Review):
    """ A Review of an Event by an Event Attendee.
    """
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name="event_reviews", verbose_name="Related Event", help_text="The event the attendee atteneded to recieve this review.")


    def __str__(self):
        return self.event.name + " : " + str(self.rating)
    
class UserProfile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=100)  
    address1 = models.CharField(max_length=255) 
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100) 
    state = models.CharField(
        max_length=2,
        choices=[
            ("AL", "Alabama"), ("AK", "Alaska"), ("AZ", "Arizona"), ("AR", "Arkansas"), ("CA", "California"),
            ("CO", "Colorado"), ("CT", "Connecticut"), ("DE", "Delaware"), ("FL", "Florida"), ("GA", "Georgia"),
            ("HI", "Hawaii"), ("ID", "Idaho"), ("IL", "Illinois"), ("IN", "Indiana"), ("IA", "Iowa"),
            ("KS", "Kansas"), ("KY", "Kentucky"), ("LA", "Louisiana"), ("ME", "Maine"), ("MD", "Maryland"),
            ("MA", "Massachusetts"), ("MI", "Michigan"), ("MN", "Minnesota"), ("MS", "Mississippi"),
            ("MO", "Missouri"), ("MT", "Montana"), ("NE", "Nebraska"), ("NV", "Nevada"), ("NH", "New Hampshire"),
            ("NJ", "New Jersey"), ("NM", "New Mexico"), ("NY", "New York"), ("NC", "North Carolina"),
            ("ND", "North Dakota"), ("OH", "Ohio"), ("OK", "Oklahoma"), ("OR", "Oregon"), ("PA", "Pennsylvania"),
            ("RI", "Rhode Island"), ("SC", "South Carolina"), ("SD", "South Dakota"), ("TN", "Tennessee"),
            ("TX", "Texas"), ("UT", "Utah"), ("VT", "Vermont"), ("VA", "Virginia"), ("WA", "Washington"),
            ("WV", "West Virginia"), ("WI", "Wisconsin"), ("WY", "Wyoming")
        ],
        verbose_name="State",
        help_text="Select your state of residence."
    )  
    zipcode = models.CharField(max_length=10) 
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True) 
    preferences = models.TextField(blank=True, null=True) 
    start_availability = models.DateField(blank=True, null=True) 
    end_availability = models.DateField(blank=True, null=True) 
    skills = models.ManyToManyField(Skill, blank=True) 

    def __str__(self):
        return f"{self.user.username}'s Profile"