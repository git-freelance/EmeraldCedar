from django.db import models
from django.shortcuts import resolve_url

from redactor.fields import RedactorField
from sorl.thumbnail import ImageField
from solo.models import SingletonModel

from core.helpers import unique_slugify, upload_common_images_to
from core.mixins import SEOModelMixin, BannerMixin
from pages.models import Page


class BlogPage(Page, SEOModelMixin, BannerMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model
    banner_text = models.CharField(max_length=100, blank=True, null=True, default='Latest Blogs')

    class Meta:
        verbose_name = 'Blog Page'

    def __str__(self):
        return 'Blog Page'

    def get_absolute_url(self):
        return resolve_url('blog')


class Post(Page, SEOModelMixin, BannerMixin):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    featured_image = ImageField(upload_to=upload_common_images_to, blank=True, null=True)
    body = RedactorField(allow_image_upload=True, allow_file_upload=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return resolve_url('blog_post', self.slug)
