from django import template

register = template.Library()

@register.filter(name='truncatechars_noellipsis')
def truncatechars_noellipsis(value, arg):
    try:
        length = int(arg)
    except ValueError:
        return value

    if not isinstance(value, str):
        value = str(value)

    return value[:length]
