from django.templatetags.cache import register


@register.filter
def m2m_fmt(value, arg):
    parts = arg.split(',')
    field_name = parts[0]
    join = parts[1] if len(parts) > 1 else " "
    sort_field = parts[2] if len(parts) > 2 else field_name
    runes = join.join([
        getattr(o, field_name)
        for o in value.all().order_by(sort_field)
    ])
    return runes


@register.filter
def order_by(value, arg):
    return value.order_by(*arg.split(','))
