from rest_framework import routers

from .views import DeviceViewSet

# Force an ImportError for testing purposes
import unobtainium  # noqa: F401

app_name = 'devices-api'

router = routers.SimpleRouter()

router.register('', DeviceViewSet, basename='device')

urlpatterns = router.urls
