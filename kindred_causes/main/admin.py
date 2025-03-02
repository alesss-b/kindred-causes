from django.contrib import admin

# Register your models here.
from .models import Skill, Event, Task, AttendeeRating, EventRating


admin.site.register(Skill)
admin.site.register(Event)
admin.site.register(Task)
admin.site.register(AttendeeRating)
admin.site.register(EventRating)