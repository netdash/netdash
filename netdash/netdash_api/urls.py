from django.conf import settings

from importlib import import_module
from rest_framework import routers

router = routers.DefaultRouter()

try:
    device_views = import_module('%s.views' % settings.NETDASH_API_DEVICE_PROVIDER)

    try:
        router.register('devices', device_views.DeviceViewSet)
    except AssertionError:
        router.register('devices', device_views.DeviceViewSet, basename='device')
    except NameError:
        pass
except AttributeError:
    pass

urlpatterns = router.urls
