import json

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, FormView
from django.urls import reverse_lazy

from core.helpers import chunks_with_reps
from core.forms import ContactForm
from core.templatetags.extras import get_gallery_with_testimonial
from django.core.mail import send_mail
from blog.models import Post
from .models import HomePage, MapPage, CustomPage, ContactPage, ThankYouPage, FeaturedProjectsPage, TestimonialsPage, \
    Testimonial, ProjectGalleryPage, GalleryCategory


import core.models


class IndexView(DetailView):
    template_name = 'core/pages/index.html'
    model = HomePage
    context_object_name = 'page'

    def get_object(self, queryset=None):
        return self.model.get_solo()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['slides'] = json.dumps([x.image.url for x in self.object.banners.all()])
        ctx['testimonials'] = self.object.section_4_testimonials.all()
        ctx['latest_posts'] = Post.objects.all()[:6]
        ctx['about_us'] = core.models.AboutUsSection.objects.all()[:6]
        ctx['statistics'] = core.models.StatisticsSection.objects.all()[:4]
        ctx['services'] = {index: service  for index, service in enumerate(core.models.Service.objects.all(), start=1)}
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
    model = core.models.Service
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['other_services'] = core.models.Service.objects.all().exclude(pk=self.object.pk).order_by('?')
        ctx['testimonials'] = self.object.testimonials.all()
        ctx['services'] = {index: service  for index, service in enumerate(core.models.Service.objects.all(), start=1)}

        return ctx


class FeaturedProjectsView(ListView):
    template_name = 'core/pages/project_new.html'
    model = core.models.FeaturedProject
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['service'] = FeaturedProjectsPage.get_solo()
        featured_projects_page_instance = FeaturedProjectsPage.get_solo()
        ctx['testimonials'] = featured_projects_page_instance.testimonials.all()
        ctx['services'] = {index: service  for index, service in enumerate(core.models.Service.objects.all(), start=1)}
        return ctx


class ProjectDetailView(DetailView):
    template_name = 'core/pages/project_detail.html'
    model = core.models.FeaturedProject
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
    template_name = 'core/pages/contact_new.html'
    form_class = ContactForm
    success_url = reverse_lazy('thankyou')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['service'] = ContactPage.get_solo()
        featured_contact_page_instance = ContactPage.get_solo()
        ctx['testimonials'] = featured_contact_page_instance.testimonials.all()
        ctx['services'] = {index: service  for index, service in enumerate(core.models.Service.objects.all(), start=1)}
        return ctx

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        try:
            form_data = self.request.POST
            subject = 'New Contact Form Submission'
            message = (
                f"User Name: {form_data.get('name')}\n"
                f"Email: {form_data.get('email')}\n"
                f"Phone: {form_data.get('phone')}\n"
                f"Best Contact Time: {form_data.get('best_contact_time')}\n"
                f"Project Address: {form_data.get('project_address')}\n\n"
                f"Message:\n{form_data.get('how_can_help')}"
            )

            from_email = 'deepansh.freelancing@gmail.com'
            recipient_list = ['vishal.mehta9123@gmail.com', 'loveagg120@gmail.com']
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print(str(e))
        return redirect('thankyou')



class ThankYouView(DetailView):
    template_name = 'core/pages/thank_you_new.html'
    model = ThankYouPage
    context_object_name = 'page'

    def get_object(self, queryset=None):
        return self.model.get_solo()
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['services'] = {index: service  for index, service in enumerate(core.models.Service.objects.all(), start=1)}
        return ctx


class TestimonialsListView(ListView):
    template_name = 'core/pages/testinomial_new.html'
    model = Testimonial
    context_object_name = 'testimonials'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page'] = TestimonialsPage.get_solo()
        return ctx


class GalleryView(DetailView):
    template_name = 'core/pages/gallery_new.html'
    model = ProjectGalleryPage
    context_object_name = 'page'

    def get_object(self, queryset=None):
        return self.model.get_solo()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch categories and images
        categories_with_images = []
        for category in self.object.categories.all():
            images = category.images.all()
            categories_with_images.append({'category': category, 'images': images})

        context['categories_with_images'] = categories_with_images

 
        context['service'] = ProjectGalleryPage.get_solo()
        context['services'] = {index: service  for index, service in enumerate(core.models.Service.objects.all(), start=1)}

        return context