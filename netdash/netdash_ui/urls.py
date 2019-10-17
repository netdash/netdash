from django.urls import path, include
from django.conf import settings

from .views import IndexView

from netdash import utils

NETDASH_MODULES = utils.create_netdash_modules(settings.NETDASH_MODULES)

module_urlpatterns = [module.ui_url for module in NETDASH_MODULES if module.ui_url]

urlpatterns = module_urlpatterns + [
    path('', IndexView.as_view(), name='home'),
    path('tellme/', include('tellme.urls')),
]
