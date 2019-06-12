from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('partials/nav.html')
def nav():
    as_tuples = settings.NETDASH_MODULE_SLUGS.items()
    indexes = [(t[0], t[1] + ':index') for t in as_tuples]
    return { 'slugs': indexes }
