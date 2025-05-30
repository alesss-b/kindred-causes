from django.contrib import admin

# Register your models here.
from .models import Skill, Event, Task, AttendeeReview, EventReview, UserProfile, AvatarOption, Notification


admin.site.register(Skill)
admin.site.register(AvatarOption)
admin.site.register(Event)
admin.site.register(Task)
admin.site.register(AttendeeReview)
admin.site.register(EventReview)
admin.site.register(UserProfile)
admin.site.register(Notification)