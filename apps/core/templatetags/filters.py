from django.template import Library


register = Library()


@register.filter
def converte_none(value):
    if not value:
        return '----------'
    return value
