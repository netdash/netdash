from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from importlib import import_module
from rest_framework import routers

device_views = import_module('netdash_device_snmp.views')

router = routers.DefaultRouter()
router.register('devices', device_views.DeviceViewSet)

urlpatterns = router.urls
