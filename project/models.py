from django.db import models


class VimeoUser(models.Model):
    name = models.CharField(max_length=255, blank=True)
    vimeo_id = models.CharField(max_length=255, unique=True)
    url = models.URLField(verify_exists=False, blank=True)
    paying = models.BooleanField(default=False)
    staffpick = models.BooleanField(default=False)
    video = models.BooleanField(default=False)