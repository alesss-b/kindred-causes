from django.contrib import admin

# Register your models here.
from .models import Skill, Event, Task, AttendeeReview, EventReview


admin.site.register(Skill)
admin.site.register(Event)
admin.site.register(Task)
admin.site.register(AttendeeReview)
admin.site.register(EventReview)