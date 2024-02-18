from django import template

register = template.Library()

@register.filter
def values_list(queryset, key):
    return queryset.values(key, flat=True)