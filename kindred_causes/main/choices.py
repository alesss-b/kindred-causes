from django.db.models import TextChoices, IntegerChoices


class EventStatus(TextChoices):
    """ Possible values for a Event status.
    """
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class EventUrgency(IntegerChoices):
    """ Possible values for Event Urgency levels.
    """
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1
