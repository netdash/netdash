from django.urls import path

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings

from netdash import utils

NETDASH_MODULES = utils.create_netdash_modules(settings.NETDASH_MODULES)

swagger_view = get_swagger_view(title='NetDash API')
schema_view = get_schema_view(title='NetDash API')

module_urlpatterns = [module.api_url for module in NETDASH_MODULES if module.api_url]

urlpatterns = module_urlpatterns + [
    path('swagger/', swagger_view, name='swagger'),
    path('', schema_view, name='schema'),
]
