from django import template


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