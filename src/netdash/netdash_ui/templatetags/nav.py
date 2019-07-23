from django import template
from django.conf import settings

from netdash.utils import get_module_slugs
from netdash_ui.urls import has_ui_urls

register = template.Library()


@register.inclusion_tag('partials/nav.html', takes_context=True)
def nav(context):
    as_tuples = get_module_slugs().items()
    indexes = [(t[0], t[1] + ':index') for t in as_tuples if has_ui_urls(t[0])]
    return {'slugs': indexes, 'login_url': settings.LOGIN_URL, 'user': context['request'].user}
