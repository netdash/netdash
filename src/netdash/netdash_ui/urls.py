from importlib import import_module

from django.urls import path

from .views import IndexView

from django.conf import settings

NETDASH_MODULES = settings.NETDASH_MODULE


def has_ui_urls(module_name):
    try:
        import_module(f'{module_name}.urls')
        return True
    except ModuleNotFoundError:
        return False


module_urlpatterns = [module.ui_app_urls for module in NETDASH_MODULES]

urlpatterns = module_urlpatterns + [
    path('', IndexView.as_view(), name='index')
]
