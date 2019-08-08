from django.urls import path

from .views import IndexView

from django.conf import settings

NETDASH_MODULES = settings.NETDASH_MODULE_OBJECTS

module_urlpatterns = [module.ui_app_urls for module in NETDASH_MODULES]

urlpatterns = module_urlpatterns + [
    path('', IndexView.as_view(), name='index')
]
