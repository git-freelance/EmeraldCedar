from django.db import models

from sorl.thumbnail import ImageField

from .helpers import upload_common_images_to


class SEOModelMixin(models.Model):
    seo_title = models.CharField(max_length=100, blank=True)
    seo_description = models.TextField(blank=True)
    seo_keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True


class BannerMixin(models.Model):
    banner = ImageField(upload_to=upload_common_images_to, blank=True, null=True)

    class Meta:
        abstract = True
