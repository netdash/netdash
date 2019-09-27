from django.urls import path, re_path
from django.conf import settings

from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as get_yasg_view
from drf_yasg import openapi

from netdash import utils, views

NETDASH_MODULES = utils.create_netdash_modules(settings.NETDASH_MODULES)

yasg_view = get_yasg_view(
    openapi.Info(
        title='NetDash API',
        default_version='v1',
    ),
)
schema_view = get_schema_view(title='NetDash API')

module_urlpatterns = [module.api_url for module in NETDASH_MODULES if module.api_url]

urlpatterns = module_urlpatterns + [
    re_path(r'^schema(?P<format>\.json|\.yaml)$', yasg_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger', yasg_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('redoc', yasg_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    path('', schema_view, name='schema'),
    path('account/login', views.login)
]
