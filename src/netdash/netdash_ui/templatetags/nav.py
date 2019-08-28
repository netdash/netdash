from django import template
from django.conf import settings
from django.contrib.auth.models import Permission

from netdash.utils import get_module_slugs
from netdash_ui.urls import has_ui_urls

register = template.Library()

PERMISSION_CODENAME = 'can_view_module'


def _can_view(user, app_label):
    perm_name = f'{app_label}.{PERMISSION_CODENAME}'
    if not Permission.objects.filter(codename=PERMISSION_CODENAME, content_type__app_label=app_label).exists():
        return True
    return user.has_perm(perm_name)


@register.inclusion_tag('partials/nav.html', takes_context=True)
def nav(context):
    as_tuples = get_module_slugs().items()
    indexes = [
            (t[0].replace('_', ' ').title(), t[1] + ':index') for t in as_tuples
            if has_ui_urls(t[0]) and _can_view(context['request'].user, t[0])
        ]
    nav_context = {
        'netdash_slugs': indexes,
        'netdash_login_url': settings.LOGIN_URL,
    }
    context.update(nav_context)
    return context
