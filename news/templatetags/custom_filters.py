from django import template
import re

register = template.Library()

@register.filter
def replace(value, arg):
    old, new = arg.split(',')
    return value.replace(old, new)

@register.filter
def cut_sentences(value, count=1):
    if not value:
        return ''
    sentences = re.split(r'(?<=[.!?])\s+', value)
    return ' '.join(sentences[:int(count)])
