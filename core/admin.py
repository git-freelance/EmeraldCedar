from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from allauth.account.models import EmailAddress
from solo.admin import SingletonModelAdmin
from mptt.admin import DraggableMPTTAdmin
from sorl.thumbnail.admin import AdminImageMixin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

from .models import FeaturedProject, ProjectImage, Service, ServiceImage, TopNavigationItem, SiteConfiguration, AboutUsSection, StatisticsSection

admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(EmailAddress)

admin.site.site_header = "Emerald Cedar Admin"
admin.site.site_title = "Emerald Cedar Admin"
admin.site.index_title = "Welcome to Emerald Cedar"


class ProjectImageInline(AdminImageMixin, admin.TabularInline):
    model = ProjectImage


@admin.register(FeaturedProject)
class FeaturedProjectAdmin(AdminImageMixin, SortableAdminMixin, admin.ModelAdmin):
    exclude = ('slug',)
    inlines = (ProjectImageInline,)

    fieldsets = (
        (None, {
            'fields': ('name', 'banner', 'featured_image', 'body_1', 'before_image', 'after_image', 'body_2',)
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )

    class Media:
        css = {
            'all': ('/static/css/admin.css',)
        }


class ServiceImageInline(AdminImageMixin, SortableInlineAdminMixin, admin.TabularInline):
    model = ServiceImage


@admin.register(Service)
class ServiceAdmin(SortableAdminMixin, AdminImageMixin, admin.ModelAdmin):
    inlines = (ServiceImageInline,)
    exclude = ('slug',)

    fieldsets = (
        (None, {
            'fields': ('name', 'image_layer', 'featured_image', 'banner', 'testimonials', 'featured_content', 'body', 'contact')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )

    class Media:
        css = {
            'all': ('/static/css/admin.css',)
        }


@admin.register(TopNavigationItem)
class TopNavigationItemAdmin(DraggableMPTTAdmin):

    def get_list_display(self, request):
        return super().list_display + ('page',)

    class Media:
        css = {
            'all': ('/static/css/admin.css',)
        }


@admin.register(SiteConfiguration)
class SiteConfiguration(AdminImageMixin, SingletonModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('email_list', 'google_maps_api_key', 'footer_scripts', 'footer_text',)
        }),
        ('About Section', {
            'fields': ('about_header', 'about_text', 'about_image', 'about_button_text', 'about_button_page')
        }),
        ('Socials', {
            'fields': ('facebook_link', 'twitter_link', 'youtube_link', 'instagram_link', 'contact_phone', 'contact_email', )
        }),
    )

    class Media:
        css = {
            'all': ('/static/css/admin.css',)
        }

admin.site.register(AboutUsSection)
admin.site.register(StatisticsSection)