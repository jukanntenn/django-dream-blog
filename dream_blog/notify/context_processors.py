def notification_count(request):
    user = request.user

    unread_count = None if user.is_anonymous else user.notifications.unread().count()

    return {"unread_count": unread_count}
