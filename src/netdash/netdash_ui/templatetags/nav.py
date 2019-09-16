from django import template
from django.conf import settings
from django.contrib.auth.models import Permission

from netdash import utils

NETDASH_MODULES = utils.create_netdash_modules(settings.NETDASH_MODULES)

register = template.Library()

PERMISSION_CODENAME = 'can_view_module'


def _can_view(user, app_label):
    perm_name = f'{app_label}.{PERMISSION_CODENAME}'
    if not Permission.objects.filter(codename=PERMISSION_CODENAME, content_type__app_label=app_label).exists():
        return True
    return user.has_perm(perm_name)


@register.inclusion_tag('partials/nav.html', takes_context=True)
def nav(context):
    indexes = [
            (module.friendly_name, module.slug + ':index') for module in NETDASH_MODULES
            if module.ui_url and _can_view(context['request'].user, module.name)
        ]
    nav_context = {
        'netdash_slugs': indexes,
        'netdash_login_url': settings.LOGIN_URL,
    }
    context.update(nav_context)
    return context
