from django.contrib import admin

from solo.admin import SingletonModelAdmin
from sorl.thumbnail.admin import AdminImageMixin
from adminsortable2.admin import SortableInlineAdminMixin
from jet.admin import CompactInline

from .models import HomePage, HomePageBanner, CustomPage, MapPage, Spot, FeaturedProjectsPage, ContactPage, \
    ThankYouPage, TestimonialsPage, Testimonial, ProjectGalleryPage, GalleryCategory, GalleryImage, ClientTestinomials


class HomePageBannerInline(AdminImageMixin, SortableInlineAdminMixin, admin.TabularInline):
    model = HomePageBanner


@admin.register(HomePage)
class HomePageAdmin(AdminImageMixin, SingletonModelAdmin):
    inlines = (HomePageBannerInline,)

    fieldsets = (
        ('Banner', {
            'fields': ('banner_header', 'banner_text', 'banner_button_1_text', 'banner_button_1_page',)
        }),
        ('Section Welcome', {
            'fields': ('section_2_background_image', 'section_2_header', 'section_2_text', 'section_2_image',
                       'section_2_button_text', 'section_2_button_page')
        }),
        ('Section Services', {
            'fields': ('section_3_background_image', 'section_3_header', 'section_3_short_description', )
        }),
        ('Section Testimonials', {
            'fields': ('section_4_header', 'section_4_testimonials',)
        }),
        ('Section About Us', {
            'fields': ('section_about_us_header', 'section_about_us_short_description', 'section_about_us_description_1', "section_about_us_description_2",)
        }),
        ('Section Blog', {
            'fields': ('section_5_header',)
        }),
        ('Section Map', {
            'fields': ('section_6_background_image', 'section_6_header', 'section_6_text', 'section_6_button_text',
                       'section_6_button_page')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )


@admin.register(CustomPage)
class CustomPageAdmin(AdminImageMixin, admin.ModelAdmin):
    exclude = ('slug',)

    fieldsets = (
        (None, {
            'fields': ('name', 'banner', 'body',)
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )

    class Media:
        css = {
            'all': ('/static/css/admin.css',)
        }


class SpotInline(AdminImageMixin, CompactInline):
    model = Spot
    readonly_fields = ('lat', 'lng')


@admin.register(MapPage)
class MapPageAdmin(AdminImageMixin, SingletonModelAdmin):
    inlines = (SpotInline,)

    fieldsets = (
        (None, {
            'fields': ('banner', 'banner_text')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )


@admin.register(FeaturedProjectsPage)
class FeaturedProjectsPageAdmin(AdminImageMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('banner', 'banner_text')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )


@admin.register(ContactPage)
class ContactPageAdmin(AdminImageMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('banner', 'banner_text')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )

    class Media:
        css = {
            'all': ('/static/css/admin.css',)
        }


@admin.register(ThankYouPage)
class ThankYouPageAdmin(AdminImageMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('banner', 'banner_text', 'body')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )

    class Media:
        css = {
            'all': ('/static/css/admin.css',)
        }


class TestimonialInline(CompactInline):
    model = Testimonial


@admin.register(TestimonialsPage)
class TestimonialsPageAdmin(AdminImageMixin, SingletonModelAdmin):
    inlines = (TestimonialInline,)
    fieldsets = (
        (None, {
            'fields': ('banner', 'banner_text',)
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )

    class Media:
        css = {
            'all': ('/static/css/admin.css',)
        }


class GalleryCategoryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = GalleryCategory


class GalleryImageInline(AdminImageMixin, admin.TabularInline):
    model = GalleryImage
    ordering = ('category',)


@admin.register(ProjectGalleryPage)
class ProjectGalleryPage(AdminImageMixin, SingletonModelAdmin):
    inlines = (GalleryCategoryInline, GalleryImageInline)

    fieldsets = (
        (None, {
            'fields': ('name', 'banner')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )

    class Media:
        css = {
            'all': ('/static/css/admin.css',)
        }


@admin.register(ClientTestinomials)
class ClientTestinomialsPage(AdminImageMixin, SingletonModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('name', 'banner', 'testimonials', 'contact')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )

    class Media:
        css = {
            'all': ('/static/css/admin.css',)
        }