from django.views.generic import TemplateView
from django.contrib.auth.models import Permission
from django.conf import settings
from netdash import utils

NETDASH_MODULES = utils.create_netdash_modules(settings.NETDASH_MODULES)

PERMISSION_CODENAME = 'can_view_module'


def _can_view(user, app_label):
    perm_name = f'{app_label}.{PERMISSION_CODENAME}'
    if not Permission.objects.filter(codename=PERMISSION_CODENAME, content_type__app_label=app_label).exists():
        return True
    return user.has_perm(perm_name)


class IndexView(TemplateView):
    template_name = 'netdash_ui/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['netdash_modules'] = [
            module for module in NETDASH_MODULES
            if module.ui_url and _can_view(self.request.user, module.name)
        ]
        return context
