from uuid import uuid4

from django.db import models


class RequestLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=128)
    user_agent = models.CharField(max_length=256)
    ip_address = models.CharField(max_length=64)
    ua_browser_family = models.CharField(max_length=64)
    ua_browser_version = models.CharField(max_length=16)
    ua_device_family = models.CharField(max_length=64)
    ua_device_model = models.CharField(max_length=32)
