from .models import UserProfile

def user_profile(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            return {'profile': profile}
        except UserProfile.DoesNotExist:
            return {'profile': None}
    return {'profile': None}

def unread_notifications_count(request):
    if request.user.is_authenticated:
        count = request.user.notifications.filter(is_read=False).count()
        return {'unread_notifications': count}
    return {'unread_notifications': 0}