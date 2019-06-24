import inspect
from importlib import import_module

from django.urls import path
from django.conf import settings
from django.conf.urls import include, url
from django.views import View

from .views import IndexView

from netdash.utils import get_module_slugs

NETDASH_MODULE_SLUGS = get_module_slugs()


def has_ui_urls(module_name):
    try:
        import_module(f'{module_name}.urls')
        return True
    except ModuleNotFoundError:
        return False


def get_url(module_name):
    slug = NETDASH_MODULE_SLUGS[module_name]
    return url(r'^' + slug + '/', include(f'{module_name}.urls', namespace=slug))

module_urlpatterns = [ get_url(module_name) for module_name in NETDASH_MODULE_SLUGS if has_ui_urls(module_name) ]

urlpatterns = module_urlpatterns + [
    path('', IndexView.as_view(), name='index')
]
