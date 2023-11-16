from django.db import models
from django.shortcuts import resolve_url

from solo.models import SingletonModel
from mptt.models import MPTTModel, TreeForeignKey
from sorl.thumbnail import ImageField, get_thumbnail as get_thumb
from redactor.fields import RedactorField

from pages.models import Page
from .mixins import SEOModelMixin, BannerMixin
from .helpers import unique_slugify, upload_common_images_to


class FeaturedProject(SEOModelMixin, BannerMixin):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    featured_image = ImageField(upload_to=upload_common_images_to, blank=True, null=True)
    body_1 = RedactorField(allow_image_upload=True, allow_file_upload=False, blank=True)

    before_image = ImageField(upload_to=upload_common_images_to, blank=True, null=True)
    after_image = ImageField(upload_to=upload_common_images_to, blank=True, null=True)

    body_2 = RedactorField(allow_image_upload=True, allow_file_upload=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return resolve_url('project', self.slug)


class ProjectImage(models.Model):
    project = models.ForeignKey(FeaturedProject, on_delete=models.CASCADE, related_name='images')
    image = ImageField(upload_to=upload_common_images_to)

    def get_thumbnail(self):
        return get_thumb(self.image, '300x300', crop='center', quality=99)


class Service(Page, SEOModelMixin, BannerMixin):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    featured_image = ImageField(upload_to=upload_common_images_to, blank=True, null=True)
    testimonials = models.ManyToManyField('pages.Testimonial', blank=True)
    body = RedactorField(allow_image_upload=True, allow_file_upload=False, blank=True)
    button_text = models.CharField(max_length=50, blank=True, null=True, verbose_name='Button text')
    button_page = models.ForeignKey('pages.Page', blank=True, null=True, on_delete=models.SET_NULL,
                                    related_name='service_button', verbose_name='Button page')

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return resolve_url('service', self.slug)


class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = ImageField(upload_to=upload_common_images_to)

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('order',)

    def get_thumbnail(self):
        return get_thumb(self.image, '300x240', crop='center', quality=99)


class TopNavigationItem(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', db_index=True,
                            on_delete=models.SET_NULL)
    page = models.ForeignKey('pages.Page', blank=True, null=True,
                             on_delete=models.SET_NULL)  # , related_name='navigation_item')
    url = models.CharField(max_length=300, blank=True, help_text='Or URL')

    class Meta:
        verbose_name = 'Top Navigation Item'
        unique_together = (('name', 'parent',),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.page:
            return resolve_url(self.page)
        elif self.url:
            return self.url
        else:
            return '#'


class SiteConfiguration(SingletonModel):
    email_list = models.TextField(blank=True, help_text='One email per line')

    google_maps_api_key = models.CharField(blank=True, max_length=200)
    footer_scripts = models.TextField(blank=True, help_text="Don't forget to wrap code in &lt;script&gt; tag")
    footer_text = models.TextField(blank=True)

    about_header = models.CharField(max_length=200, blank=True, verbose_name='Header')
    about_text = models.TextField(blank=True, verbose_name='Text')
    about_image = ImageField(upload_to=upload_common_images_to, blank=True, null=True, verbose_name='Image')
    about_button_text = models.CharField(max_length=50, blank=True, null=True, verbose_name='Button text')
    about_button_page = models.ForeignKey('pages.Page', blank=True, null=True, on_delete=models.SET_NULL,
                                          related_name='about_siteconfiguration', verbose_name='Button page')

    contact_phone = models.CharField(max_length=100, blank=True, verbose_name="Phone Number")
    # contact_address = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True, verbose_name="Email Address")

    # working_hours = models.TextField(blank=True)

    facebook_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    youtube_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Site Configuration'

    def __str__(self):
        return 'Site Configuration'


class AboutUsSection(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name='Header')
    description = models.TextField(blank=True, verbose_name='description')
    image = ImageField(upload_to=upload_common_images_to, blank=True, null=True, verbose_name='Image')

    class Meta:
        verbose_name = 'About Us'

    def __str__(self):
        return self.title


class StatisticsSection(models.Model):
    value = models.CharField(max_length=200, blank=True, verbose_name='Value')
    title = models.TextField(blank=True, verbose_name='Title')

    class Meta:
        verbose_name = 'Statistics'

    def __str__(self):
        return self.title