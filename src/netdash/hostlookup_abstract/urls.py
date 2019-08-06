from django.conf.urls import url

from .views import BaseHostLookupView

app_name = 'hostlookup'
urlpatterns = [
    url(r'^$', BaseHostLookupView.as_view(), name='index')
]