from django import template
import calendar
from datetime import datetime

register = template.Library()


@register.filter
def month_name_2(month_number):
    month_number = int(month_number)
    return calendar.month_name[month_number]



@register.filter
def get_item_(queryset, year):
    """Filters summary_data by year."""
    return [item for item in queryset if item['date'].year == year]


@register.filter
def month_name(month_num):
    return datetime(2000, month_num, 1).strftime('%B')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, {})

@register.filter
def items(dictionary):
    return dictionary.items()


@register.filter
def blank_if_0(amnt):
    if amnt == 0.0:
        return ""
    return amnt


@register.filter
def as_absolute(amnt):
    #a = f"u'\u20b5'"
    a = amnt * -1
    return "{:,.2f}".format(a)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])


@register.filter
def get_item_1(dict_obj, key):
    if dict_obj is None:
        return []
    return dict_obj.get(int(key), [])


@register.simple_tag
def get_programs(programs, month, dept):
    return [p for p in programs if int(p['date'].month) == int(month) and p['department__name'] == dept]