from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from importlib import import_module
from rest_framework import routers

router = routers.DefaultRouter()

try:
    device_views = import_module(
        '%s.views' % settings.NETDASH_API_DEVICE_PROVIDER)

    try:
        router.register('devices', device_views.DeviceViewSet)
    except AssertionError:
        router.register(
            'devices', device_views.DeviceViewSet, basename='device')
    except NameError:
        pass
except AttributeError:
    raise ImproperlyConfigured('NETDASH_API_DEVICE_PROVIDER must be set')
except ModuleNotFoundError:
    raise ImproperlyConfigured(
        'Could not import views from %s (Is that package installed?) '
        '(Specificed in NETDASH_API_DEVICE_PROVIDER.)' %
        settings.NETDASH_API_DEVICE_PROVIDER)

urlpatterns = router.urls
