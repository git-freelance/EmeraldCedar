from django.db import models
from django.shortcuts import resolve_url

from solo.models import SingletonModel
from redactor.fields import RedactorField
from sorl.thumbnail import ImageField, get_thumbnail as get_thumb

from core.mixins import SEOModelMixin, BannerMixin
from core.helpers import unique_slugify, upload_common_images_to


class Page(models.Model):
    pid = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model

    def __str__(self):
        if hasattr(self, 'homepage'):
            return str(self.homepage)
        elif hasattr(self, 'custompage'):
            return f'Custom Page: {self.custompage}'
        elif hasattr(self, 'service'):
            return f'Service Page: {self.service}'
        elif hasattr(self, 'mappage'):
            return str(self.mappage)
        elif hasattr(self, 'featuredprojectspage'):
            return str(self.featuredprojectspage)
        elif hasattr(self, 'contactpage'):
            return str(self.contactpage)
        elif hasattr(self, 'thankyoupage'):
            return str(self.thankyoupage)
        elif hasattr(self, 'blogpage'):
            return str(self.blogpage)
        elif hasattr(self, 'post'):
            return str(self.post)
        elif hasattr(self, 'testimonialspage'):
            return str(self.testimonialspage)
        elif hasattr(self, 'projectgallerypage'):
            return str(self.projectgallerypage)
        else:
            return '<Page %s>' % self.pid

    def get_absolute_url(self):
        if hasattr(self, 'homepage'):
            return resolve_url(self.homepage)
        elif hasattr(self, 'custompage'):
            return resolve_url(self.custompage)
        elif hasattr(self, 'service'):
            return resolve_url(self.service)
        elif hasattr(self, 'mappage'):
            return resolve_url(self.mappage)
        elif hasattr(self, 'featuredprojectspage'):
            return resolve_url(self.featuredprojectspage)
        elif hasattr(self, 'contactpage'):
            return resolve_url(self.contactpage)
        elif hasattr(self, 'thankyoupage'):
            return resolve_url(self.thankyoupage)
        elif hasattr(self, 'blogpage'):
            return resolve_url(self.blogpage)
        elif hasattr(self, 'post'):
            return resolve_url(self.post)
        elif hasattr(self, 'testimonialspage'):
            return resolve_url(self.testimonialspage)
        elif hasattr(self, 'projectgallerypage'):
            return resolve_url(self.projectgallerypage)
        else:
            return '#'


class HomePage(Page, SEOModelMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model

    banner_text = models.TextField(blank=True)
    banner_header = models.CharField(max_length=200, blank=True, verbose_name="Banner Title")
    banner_button_1_text = models.CharField(max_length=50, blank=True, null=True, verbose_name='Button 1 text')
    banner_button_1_page = models.ForeignKey('pages.Page', blank=True, null=True, on_delete=models.SET_NULL,
                                             related_name='banner_button_1_homepage', verbose_name='Button 1 page')

    section_2_background_image = ImageField(upload_to=upload_common_images_to, blank=True, null=True,
                                            verbose_name='Background image')
    section_2_header = models.CharField(max_length=200, blank=True, verbose_name='Header')
    section_2_text = models.TextField(blank=True, verbose_name='Text')
    section_2_image = ImageField(upload_to=upload_common_images_to, blank=True, null=True, verbose_name='Image')
    section_2_button_text = models.CharField(max_length=50, blank=True, null=True, verbose_name='Button text')
    section_2_button_page = models.ForeignKey('pages.Page', blank=True, null=True, on_delete=models.SET_NULL,
                                              related_name='section_2_homepage', verbose_name='Button page')

    section_3_background_image = ImageField(upload_to=upload_common_images_to, blank=True, null=True,
                                            verbose_name='Background image')
    section_3_short_description = models.CharField(max_length=200, blank=True, verbose_name='Short Description')
    section_3_header = models.CharField(max_length=200, blank=True, verbose_name='Header')

    section_4_header = models.CharField(max_length=200, blank=True, verbose_name='Header')
    section_4_testimonials = models.ManyToManyField('pages.Testimonial', blank=True, related_name='homepage')

    section_5_header = models.CharField(max_length=200, blank=True, verbose_name='Header')

    section_6_background_image = ImageField(upload_to=upload_common_images_to, blank=True, null=True,
                                            verbose_name='Background image')
    section_6_header = models.CharField(max_length=200, blank=True, verbose_name='Header')
    section_6_text = models.TextField(blank=True, verbose_name='Text')
    section_6_button_text = models.CharField(max_length=50, blank=True, null=True, verbose_name='Button text')
    section_6_button_page = models.ForeignKey('pages.Page', blank=True, null=True, on_delete=models.SET_NULL,
                                              related_name='section_6_homepage', verbose_name='Button page')
    section_about_us_description_1 = models.TextField(blank=True, verbose_name='Description 1')
    section_about_us_description_2 = models.TextField(blank=True, verbose_name='Description 2')
    section_about_us_short_description = models.TextField(blank=True, verbose_name='Short Description')
    section_about_us_header = models.CharField(max_length=200, blank=True, verbose_name='Section Header')

    class Meta:
        verbose_name = 'Home Page'

    def __str__(self):
        return 'Home Page'

    def get_absolute_url(self):
        return resolve_url('index')


class HomePageBanner(models.Model):
    home_page = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name='banners')
    image = ImageField(upload_to=upload_common_images_to, blank=True, null=True)

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        verbose_name = 'Home Banner'
        ordering = ('order',)

    def __str__(self):
        return self.image.name


class CustomPage(Page, SEOModelMixin, BannerMixin):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    body = RedactorField(allow_image_upload=True, allow_file_upload=False, blank=True)

    class Meta:
        verbose_name = 'Custom Page'
        verbose_name_plural = 'Custom Pages'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return resolve_url('custom_page', self.slug)


class MapPage(Page, SEOModelMixin, BannerMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model
    banner_text = models.CharField(max_length=100, blank=True, null=True, default='Areas We Serve')

    class Meta:
        verbose_name = 'Map Page'

    def __str__(self):
        return 'Map Page'

    def get_absolute_url(self):
        return resolve_url('map')


class Spot(models.Model):
    mappage = models.ForeignKey(MapPage, on_delete=models.CASCADE, related_name='spots')

    address = models.CharField(max_length=200, blank=True)
    image = ImageField(upload_to=upload_common_images_to, blank=True, null=True)
    text = models.CharField(max_length=200, blank=True)
    project = models.OneToOneField('core.FeaturedProject', blank=True, null=True, on_delete=models.SET_NULL)
    # TODO Admin QS Filter used projects

    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.address

    def get_thumbnail(self):
        return get_thumb(self.image, '75x75', crop='center', quality=99)


class FeaturedProjectsPage(Page, SEOModelMixin, BannerMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model
    banner_text = models.CharField(max_length=100, blank=True, null=True, default='Featured Projects')
    testimonials = models.ManyToManyField('pages.Testimonial', blank=True)
    contact = RedactorField(allow_image_upload=False, allow_file_upload=False, blank=True)

    class Meta:
        verbose_name = 'Featured Projects Page'

    def __str__(self):
        return 'Featured Projects Page'

    def get_absolute_url(self):
        return resolve_url('featured_projects')


class ContactPage(Page, SEOModelMixin, BannerMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model
    banner_text = models.CharField(max_length=100, blank=True, null=True, default='Contact Us')
    body = RedactorField(allow_image_upload=True, allow_file_upload=False, blank=True)

    class Meta:
        verbose_name = 'Contact Page'

    def __str__(self):
        return 'Contact Page'

    def get_absolute_url(self):
        return resolve_url('contact')


class ThankYouPage(Page, SEOModelMixin, BannerMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model
    banner_text = models.CharField(max_length=100, blank=True, null=True, default='Thank You')
    body = RedactorField(allow_image_upload=True, allow_file_upload=False, blank=True)

    class Meta:
        verbose_name = 'Thank You Page'

    def __str__(self):
        return 'Thank You Page'

    def get_absolute_url(self):
        return resolve_url('thankyou')


class TestimonialsPage(Page, SEOModelMixin, BannerMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model
    banner_text = models.CharField(max_length=100, blank=True, null=True, default="Client's Testimonials")

    class Meta:
        verbose_name = 'Testimonials Page'

    def __str__(self):
        return 'Testimonials Page'

    def get_absolute_url(self):
        return resolve_url('testimonials')


class Testimonial(models.Model):
    testimonial_page = models.ForeignKey(TestimonialsPage, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True, default='House Owner')
    user_image = ImageField(upload_to=upload_common_images_to, blank=True, null=True, verbose_name='User Image')

    def __str__(self):
        return self.text[:20] + '...'


class ProjectGalleryPage(Page, SEOModelMixin, BannerMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model
    # banner_text = models.CharField(max_length=100, blank=True, null=True, default='Gallery')
    testimonials = models.ManyToManyField('pages.Testimonial', blank=True)

    class Meta:
        verbose_name = 'Project Gallery Page'

    def __str__(self):
        return 'Project Gallery Page'

    def get_absolute_url(self):
        return resolve_url('gallery')


class GalleryCategory(models.Model):
    gallery_page = models.ForeignKey(ProjectGalleryPage, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100, unique=True)

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class GalleryImage(models.Model):
    gallery_page = models.ForeignKey(ProjectGalleryPage, on_delete=models.CASCADE, related_name='images')
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images')
    image = ImageField(upload_to=upload_common_images_to)

    def get_thumbnail(self):
        return get_thumb(self.image, '300x300', crop='center', quality=99)
