from django.conf.urls import url

from .views import index


app_name = 'hostlookup'
urlpatterns = [
    url(r'^$', index, name='index'),
    # Add routes for your views here...
]
