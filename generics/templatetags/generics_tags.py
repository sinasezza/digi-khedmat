from django import template
from django.template.defaultfilters import date as django_date
import jdatetime

register = template.Library()

