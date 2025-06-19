from .models import Notification, Member


def notification_context(request):
    if request.user.is_authenticated and hasattr(request.user, "member"):
        member = Member.objects.filter(user=request.user).first()
        notifications = (
            Notification.objects.filter(member=member).all().order_by("-created_at")
        )
        unread_notifications_count = [
            notif for notif in notifications if not notif.is_read
        ]
        return {
            "notifications": notifications,
            "unread_notifications_count": unread_notifications_count,
        }
    return {}
