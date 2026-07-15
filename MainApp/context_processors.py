from .models import Activity

def notifications(request):
    if request.user.is_authenticated:
        activitys = Activity.objects.all()[:5]
        unread_count = activitys.count()

        return {
            "notifications": activitys,
            "notification_count": unread_count,
        }
    
    return {}
