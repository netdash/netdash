from django.conf.urls import url

from .views import index

# app_name = 'devices'  # Do not set app_name to test informational messages
urlpatterns = [
    url(r'^$', index, name='index')
]
