from django.template import Library
import datetime

register = Library()


@register.filter
def stringformat(value, args):
    return datetime.datetime.strftime(value, args)
