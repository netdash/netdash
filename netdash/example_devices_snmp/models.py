from django.db import models


class SnmpDevice(models.Model):
    hostname = models.CharField(max_length=100)

    def __str__(self):
        return self.hostname
