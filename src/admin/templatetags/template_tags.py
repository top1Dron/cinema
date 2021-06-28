from django import template
from django.utils.translation import ugettext_lazy as _


register = template.Library()


@register.simple_tag
def get_hall_row_places(hall, row):
    return hall.ordered_places.filter(real_row=row)


@register.simple_tag
def define(val=None):
    return val

@register.simple_tag
def get_ticket_from_place(session, place):
    return session.tickets.get(place=place)


@register.filter()
def sec_to_ms(value):
    return str(int(value) * 1000)


@register.filter()
def duration(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    if not hours or hours >= 5:
        hours_str = _('часов')
    elif hours == 1:
        hours_str = _('час')
    elif hours > 1 and hours < 5:
        hours_str = _('часа')

    if not minutes or minutes >= 5:
        minutes_str = _('минут')
    elif minutes == 1:
        minutes_str = _('минута')
    elif minutes > 1 and minutes < 5:
        minutes_str = _('минуты')

    return f'{hours} {hours_str} {minutes} {minutes_str}'