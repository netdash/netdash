from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from importlib import import_module
from rest_framework import routers

from .views import HostViewSet

app_name = 'devices-api'

router = routers.SimpleRouter()

router.register('', HostViewSet, basename='host')

urlpatterns = router.urls
