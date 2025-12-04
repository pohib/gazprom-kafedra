from django import template
import datetime
from calendar import monthrange
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def month_has_events(month_num, events):
    return events.filter(event_date_start__month=month_num).exists()

@register.filter
def day_has_events(day_num, events):
    return events.filter(event_date_start__day=day_num).exists()
