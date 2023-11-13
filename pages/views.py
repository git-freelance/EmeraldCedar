import json

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, FormView
from django.urls import reverse_lazy

from core.helpers import chunks_with_reps
from core.models import FeaturedProject, Service
from core.forms import ContactForm
from core.templatetags.extras import get_gallery_with_testimonial

from blog.models import Post
from .models import HomePage, MapPage, CustomPage, ContactPage, ThankYouPage, FeaturedProjectsPage, TestimonialsPage, \
    Testimonial, ProjectGalleryPage, GalleryCategory


class IndexView(DetailView):
    template_name = 'core/pages/index.html'
    model = HomePage
    context_object_name = 'page'

    def get_object(self, queryset=None):
        return self.model.get_solo()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['slides'] = json.dumps([x.image.url for x in self.object.banners.all()])
        ctx['services'] = Service.objects.all()
        ctx['testimonials'] = self.object.section_4_testimonials.all()
        ctx['latest_posts'] = Post.objects.all()[:6]
        return ctx


class MapDetailView(DetailView):
    template_name = 'core/pages/map.html'
    model = MapPage
    context_object_name = 'page'

    def get_object(self, queryset=None):
        return self.model.get_solo()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['spots_json'] = json.dumps([{'lat': x.lat,
                                         'lng': x.lng,
                                         'text': x.text,
                                         'image': x.get_thumbnail().url if x.image else None,
                                         'url': x.project.get_absolute_url() if x.project else None} for x in
                                        self.object.spots.all()])
        return ctx


class ServiceDetailView(DetailView):
    template_name = 'core/pages/service_detail.html'
    model = Service
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['other_services'] = Service.objects.all().exclude(pk=self.object.pk).order_by('?')
        return ctx


class FeaturedProjectsView(ListView):
    template_name = 'core/pages/featured_projects.html'
    model = FeaturedProject
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page'] = FeaturedProjectsPage.get_solo()
        return ctx


class ProjectDetailView(DetailView):
    template_name = 'core/pages/project_detail.html'
    model = FeaturedProject
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['photos_chunks'] = chunks_with_reps(self.object.images.all(), 2)
        return ctx


class CustomPageDetailView(DetailView):
    template_name = 'core/pages/custom_page.html'
    model = CustomPage
    context_object_name = 'page'


class ContactView(FormView):
    template_name = 'core/pages/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('thankyou')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page'] = ContactPage.get_solo()
        return ctx

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class ThankYouView(DetailView):
    template_name = 'core/pages/thank_you.html'
    model = ThankYouPage
    context_object_name = 'page'

    def get_object(self, queryset=None):
        return self.model.get_solo()


class TestimonialsListView(ListView):
    template_name = 'core/pages/testimonials.html'
    model = Testimonial
    context_object_name = 'testimonials'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page'] = TestimonialsPage.get_solo()
        return ctx


class GalleryView(DetailView):
    template_name = 'core/pages/gallery.html'
    model = ProjectGalleryPage
    context_object_name = 'page'

    def get_object(self, queryset=None):
        return self.model.get_solo()

    def get(self, request, *args, **kwargs):
        ret = super().get(request, *args, **kwargs)
        category_id = request.GET.get('category_id')
        if category_id:# and request.is_ajax():
            category = get_object_or_404(GalleryCategory, pk=category_id)
            rendered = get_gallery_with_testimonial(photos=category.images.all(),
                                                    testimonials=self.object.testimonials.all())
            return render(request, 'core/partials/gallery_with_testimonial.html', rendered)
        else:
            return ret
