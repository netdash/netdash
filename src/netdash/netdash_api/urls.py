import inspect
from importlib import import_module

from django.urls import path
from django.conf import settings
from django.conf.urls import include, url

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view

from netdash.utils import get_module_slugs

swagger_view = get_swagger_view(title='NetDash API')
schema_view = get_schema_view(title='NetDash API')

NETDASH_MODULE_SLUGS = get_module_slugs()


def has_api_urls(module_name):
    try:
        import_module(f'{module_name}.api.urls')
        return True
    except ModuleNotFoundError:
        return False


def get_url(module_name):
    slug = NETDASH_MODULE_SLUGS[module_name]
    return url(r'^' + slug + '/', include(f'{module_name}.api.urls'))

module_urlpatterns = [ get_url(module_name) for module_name in NETDASH_MODULE_SLUGS if has_api_urls(module_name) ]

urlpatterns = module_urlpatterns + [
    path('swagger/', swagger_view, name='swagger'),
    path('', schema_view, name='schema'),
]
