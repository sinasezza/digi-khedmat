import jdatetime
from django import template

register = template.Library()

@register.filter
def  to_jdate(date, arg=None):
        return jdatetime.date.fromgregorian(day=date.day, month=date.month, year=date.year)