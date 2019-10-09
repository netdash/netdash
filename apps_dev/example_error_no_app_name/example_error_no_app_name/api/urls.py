from rest_framework import routers

from .views import DeviceViewSet

# app_name = 'devices-api'  # Do not set app_name to test informational messages

router = routers.SimpleRouter()

router.register('', DeviceViewSet, basename='device')

urlpatterns = router.urls
