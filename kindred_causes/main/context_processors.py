from .models import UserProfile

def user_profile(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            return {'profile': profile}
        except UserProfile.DoesNotExist:
            return {'profile': None}
    return {'profile': None}