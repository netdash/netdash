from rest_framework import routers

from .views import DeviceViewSet

app_name = 'devices-api'

router = routers.SimpleRouter()

router.register('', DeviceViewSet, basename='device')

urlpatterns = router.urls
