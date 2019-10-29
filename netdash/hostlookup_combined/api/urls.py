from rest_framework import routers

from .views import HostlookupCombinedViewSet

app_name = 'hostlookup-api'

router = routers.SimpleRouter()

router.register('', HostlookupCombinedViewSet, basename='hosts')

urlpatterns = router.urls
