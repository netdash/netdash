import inspect
from importlib import import_module

from django.urls import path
from django.conf import settings
from django.conf.urls import include, url

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view

swagger_view = get_swagger_view(title='NetDash API')
schema_view = get_schema_view(title='NetDash API')


def get_url(module_name):
    slug = settings.NETDASH_MODULE_SLUGS[module_name]
    return url(r'^' + slug + '/', include(f'{module_name}.api.urls'))

module_urlpatterns = [ get_url(module_name) for module_name in settings.NETDASH_MODULE_SLUGS ]

urlpatterns = module_urlpatterns + [
    path('swagger/', swagger_view),
    path('', schema_view),
]
