from rest_framework import routers

from .views import DeviceViewSet

import unobtainium  # Force an ImportError for testing purposes

app_name = 'devices-api'

router = routers.SimpleRouter()

router.register('', DeviceViewSet, basename='device')

urlpatterns = router.urls
