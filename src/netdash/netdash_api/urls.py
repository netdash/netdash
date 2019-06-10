import inspect
from importlib import import_module

from django.conf import settings

from rest_framework import routers, viewsets

router = routers.DefaultRouter()

for module_name in settings.NETDASH_MODULE_SLUGS:
    module = import_module(module_name)
    slug = settings.NETDASH_MODULE_SLUGS[module_name]
    view_module = import_module(f'{module_name}.views')
    viewsets = [x[1] for x in inspect.getmembers(view_module, lambda m: inspect.isclass(m) and issubclass(m, viewsets.ViewSet))]
    for v in viewsets:
        print('registering viewset', v)
        router.register(slug, v, basename=getattr(v, 'basename', False) or slug)

urlpatterns = router.urls
