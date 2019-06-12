from django.conf.urls import url

from .views import DeviceList

app_name = 'devices'
urlpatterns = [
    url(r'^$', DeviceList.as_view(), name='index')
]
