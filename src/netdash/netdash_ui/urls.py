import inspect
from importlib import import_module

from django.urls import path
from django.conf import settings
from django.conf.urls import include, url
from django.views import View

from .views import IndexView


def get_url(module_name):
    slug = settings.NETDASH_MODULE_SLUGS[module_name]
    return url(r'^' + slug + '/', include(f'{module_name}.urls', namespace=slug))

module_urlpatterns = [ get_url(module_name) for module_name in settings.NETDASH_MODULE_SLUGS]

urlpatterns = module_urlpatterns + [
    path('', IndexView.as_view(), name='index')
]
