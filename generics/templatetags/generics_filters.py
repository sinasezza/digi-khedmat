from jalali_date import datetime2jalali, date2jalali
from django import template


register = template.Library()


@register.filter
def  to_Jdate(date, arg=None):
    # return jdatetime.date.fromgregorian(day=date.day, month=date.month, year=date.year).strftime('%Y/%m/%d')
    return date2jalali(date).strftime('%Y/%m/%d')

# -------------------------------------------------------------------------------------

@register.filter
def to_Jdatetime(date, arg=None):
    return datetime2jalali(date).strftime('%Y/%m/%d - %H:%M:%S')
