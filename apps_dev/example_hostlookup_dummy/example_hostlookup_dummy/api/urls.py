from django.conf import settings

from rest_framework import routers

from .views import HostViewSet

app_name = 'hostlookup-api'

router = routers.SimpleRouter()

router.register('', HostViewSet, basename='host')

urlpatterns = router.urls
