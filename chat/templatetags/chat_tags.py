from django import template
from .. import models


register = template.Library()


@register.simple_tag
def get_other_user(user, thread):
    return  thread.user1 if thread.user2 == user else thread.user2