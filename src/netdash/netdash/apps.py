from django.apps import AppConfig
from django.conf import settings

import .utils


class NetdashConfig(AppConfig):
    name = 'netdash'

    def ready(self):
        setattr(settings, 'NETDASH_MODULE_OBJECTS', utils.create_netdash_modules()
