from importlib import import_module

from django.urls import path

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings

NETDASH_MODULES = settings.NETDASH_MODULE_OBJECTS


swagger_view = get_swagger_view(title='NetDash API')
schema_view = get_schema_view(title='NetDash API')


def has_api_urls(module_name):
    try:
        import_module(f'{module_name}.api.urls')
        return True
    except ModuleNotFoundError:
        return False


module_urlpatterns = [module.api_app_urls for module in NETDASH_MODULES]

urlpatterns = module_urlpatterns + [
    path('swagger/', swagger_view, name='swagger'),
    path('', schema_view, name='schema'),
]
