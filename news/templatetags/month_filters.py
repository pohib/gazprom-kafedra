from django import template

register = template.Library()

@register.filter
def get_month_name(month_num):
    MONTH_NAMES = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
        5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
        9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }
    try:
        return MONTH_NAMES.get(int(month_num), '')
    except (ValueError, TypeError):
        return ''