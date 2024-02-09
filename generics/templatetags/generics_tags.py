import jdatetime
from django import template


register = template.Library()


@register.inclusion_tag(filename='partials/sidebar.html')
def load_sidebar(request):
    notifications = request.user.notifications.all()
    
    context = {
        'notifications': notifications,
    }
    return context