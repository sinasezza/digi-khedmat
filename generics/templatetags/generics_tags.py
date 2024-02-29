import jdatetime
from django import template


register = template.Library()


@register.inclusion_tag(filename='partials/sidebar.html')
def load_sidebar(request):
    unseen_notifications_count = request.user.notifications.unseen_notifications().count()
    favorites_count = request.user.favorites.count()
    resumes_count = request.user.rcv_resumes.count() + request.user.rcv_resume_files.count()
    
    context = {
        'unseen_notifications_count': unseen_notifications_count,
        'favorites_count': favorites_count,
        'resumes_count': resumes_count,
        'user': request.user,
    }
    return context

# -----------------------------------------------------------------------

@register.simple_tag
def get_notifications_count(request):
    return request.user.notifications.unseen_notifications().count()

# -----------------------------------------------------------------------