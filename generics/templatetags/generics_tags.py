import jdatetime
from django import template


register = template.Library()


@register.inclusion_tag(filename='partials/sidebar.html')
def load_sidebar(request):
    unseen_notifications_count = request.user.notifications.unseen_notifications().count()
    
    context = {
        'unseen_notifications_count': unseen_notifications_count,
    }
    return context