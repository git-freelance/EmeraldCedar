from django.contrib import admin

from solo.admin import SingletonModelAdmin
from sorl.thumbnail.admin import AdminImageMixin

from .models import BlogPage, Post


@admin.register(BlogPage)
class BlogPageAdmin(AdminImageMixin, SingletonModelAdmin):

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


@admin.register(Post)
class PostAdmin(AdminImageMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'banner', 'featured_image', 'body')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )

    class Media:
        css = {
            'all': ('/static/css/admin.css',)
        }

