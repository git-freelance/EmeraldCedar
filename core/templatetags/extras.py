import re

from django import template
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags

from authorization.models import Project
from core.helpers import chunks
import core.models

register = template.Library()


@register.inclusion_tag('core/partials/header.html', takes_context=True)
def get_nav_top(context):
    return {'request': context['request'],
            'nodes': core.models.TopNavigationItem.objects.all().select_related('parent', 'page')}


@register.inclusion_tag('core/partials/header-new.html', takes_context=True)
def get_nav_top_new(context):
    return {'request': context['request'],
            'nodes': core.models.TopNavigationItem.objects.all().select_related('parent', 'page'),
            "services": core.models.Service.objects.all() }


@register.inclusion_tag('core/partials/footer-new.html', takes_context=True)
def get_nav_bottom_new(context):
    return {'request': context['request'],
            'nodes': core.models.TopNavigationItem.objects.all().select_related('parent', 'page')}


@register.inclusion_tag('core/partials/service_box.html')
def get_service_box(service):
    return {'service': service}

@register.inclusion_tag('core/partials/service_box_new.html')
def get_service_box_new(service, position):
    position = 'left' if int(position%2) else 'right'
    return {'service': service, "position": position}


@register.inclusion_tag('core/partials/testimonial_new_box.html')
def get_testimonialbox_new(testimonial, position):
    position = 'left' if int(position%2) else 'right'
    return {'testimonial': testimonial, "position": position}

@register.inclusion_tag('core/partials/gallery_with_testimonial.html')
def get_gallery_with_testimonial(photos, category=None):
    return {'photos_chunks': chunks(photos, 7), 'category': category}


@register.inclusion_tag('core/partials/gallery_row.html')
def get_gallery_row(photos, testimonials=None):
    return {'photos': photos, 'testimonials': testimonials}


@register.inclusion_tag('core/partials/testi_box_in_gallery.html')
def get_testi_box_in_gallery(testimonials, h2x=False):
    return {'testimonials': testimonials, 'h2x': h2x}


@register.inclusion_tag('core/partials/post_box.html')
def get_post_box(post):
    return {'post': post}


@register.inclusion_tag('core/partials/section_about.html', takes_context=True)
def get_about_section(context):
    site_config = context['site_config']
    return {'header': site_config.about_header,
            'text': site_config.about_text,
            'image': site_config.about_image,
            'button_text': site_config.about_button_text,
            'button_page': site_config.about_button_page}


@register.inclusion_tag('authorization/partials/dash_sidebar.html', takes_context=True)
def get_dash_sidebar(context):
    request = context['request']
    if request.user.is_admin():
        projects = Project.objects.all()
    else:
        projects = request.user.projects.all()
    return {'request': request, 'projects': projects}


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter
def splitlines(string):
    return mark_safe('<br>'.join(string.split()))


@register.filter
def striptags2(text):
    base_patterns = {
        '&[rl]dquo;': '',
        '&[rl]squo;': '',
        '&nbsp;': ' ',
        '&lt;': '<',
        '&gt;': '>',
    }

    final_text = strip_tags(text)
    for pattern, repl in base_patterns.items():
        final_text = re.sub(pattern, repl, final_text)
    return final_text
