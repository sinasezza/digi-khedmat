import jdatetime
from django import template


register = template.Library()


@register.inclusion_tag(filename='partials/sidebar.html')
def load_sidebar(request):
    notifications = request.user.notifications.all()
    unread_notifications = notifications.filter(unread=True)
    sidebar_count = unread_notifications.count()
    context = {
        'notifications': unread_notifications,
        'sidebar_count': sidebar_count,
    }
    return context