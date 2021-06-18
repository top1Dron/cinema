from django import template


register = template.Library()


@register.simple_tag
def get_hall_row_places(hall, row):
    return hall.ordered_places.filter(real_row=row)


@register.simple_tag
def define(val=None):
  return val