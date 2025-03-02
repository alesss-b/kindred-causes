from django.db import models
from django.contrib.auth.models import User


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