from importlib import import_module

from django.urls import path, re_path
from django.conf.urls import include, url

from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as get_yasg_view
from drf_yasg import openapi

from netdash.utils import get_module_slugs

yasg_view = get_yasg_view(
    openapi.Info(
        title='NetDash API',
        default_version='v1',
    ),
)
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


module_urlpatterns = [get_url(module_name) for module_name in NETDASH_MODULE_SLUGS if has_api_urls(module_name)]

urlpatterns = module_urlpatterns + [
    re_path(r'^schema(?P<format>\.json|\.yaml)$', yasg_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger', yasg_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('redoc', yasg_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    path('', schema_view, name='schema'),
]
