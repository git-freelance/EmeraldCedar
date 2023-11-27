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
    Testimonial, ProjectGalleryPage, GalleryCategory, ClientTestinomials, Testimonial


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
    
    def post(self, request, *args, **kwargs):
        try:
            form_data = self.request.POST
            subject = 'New Service Enquiry'
            message = (
                f"User Name: {form_data.get('user_name')}\n"
                f"Email: {form_data.get('email')}\n"
                f"Phone: {form_data.get('phone')}\n"
                f"Service Enquired for: {form_data.get('services_intrest')}\n"
                f"Postal code: {form_data.get('head_with_postal_code')}\n\n"
                f"Project Description:\n{form_data.get('project_description')}"
            )
            from_email = 'deepansh.freelancing@gmail.com'
            recipient_list = ['vishal.mehta9123@gmail.com', 'bogdan@webreign.ca']
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print(str(e))
        return redirect('thankyou')


class FeaturedProjectsView(ListView):
    template_name = 'core/pages/project_new.html'
    model = core.models.FeaturedProject
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['service'] = FeaturedProjectsPage.get_solo()
        featured_projects_page_instance = FeaturedProjectsPage.get_solo()
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
                f"Service Enquired for: {form_data.get('services_intrest')}\n"
                f"Postal code: {form_data.get('head_with_postal_code')}\n\n"
                f"Project Description:\n{form_data.get('project_description')}"
            )

            from_email = 'deepansh.freelancing@gmail.com'
            recipient_list = ['bogdan@webreign.ca']
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
        ctx['service'] = ClientTestinomials.get_solo()
        ctx['testimonial'] = {index: service  for index, service in enumerate(Testimonial.objects.all(), start=1)}
        ctx['services'] = {index: service  for index, service in enumerate(core.models.Service.objects.all(), start=1)}
        return ctx
    
    def post(self, request, *args, **kwargs):
        try:
            form_data = self.request.POST
            subject = 'New Service Enquiry'
            message = (
                f"User Name: {form_data.get('user_name')}\n"
                f"Email: {form_data.get('email')}\n"
                f"Phone: {form_data.get('phone')}\n"
                f"Service Enquired for: {form_data.get('services_intrest')}\n"
                f"Postal code: {form_data.get('head_with_postal_code')}\n\n"
                f"Project Description:\n{form_data.get('project_description')}"
            )
            from_email = 'deepansh.freelancing@gmail.com'
            recipient_list = ['vishal.mehta9123@gmail.com', 'bogdan@webreign.ca']
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print(str(e))
        return redirect('thankyou')


class GalleryView(DetailView):
    template_name = 'core/pages/gallery_new.html'
    model = ProjectGalleryPage
    context_object_name = 'page'

    def get_object(self, queryset=None):
        return self.model.get_solo()

    def get(self, request, *args, **kwargs):
        ret = super().get(request, *args, **kwargs)
        category_id = request.GET.get('category_id')
        if category_id:
            category = get_object_or_404(GalleryCategory, pk=category_id)
            rendered = get_gallery_with_testimonial(photos=category.images.all(), category=category)
            return render(self.request, 'core/partials/gallery_with_testimonial.html', rendered)
        else:
            category = self.object.categories.order_by('id').first()
            categories_with_images = []
            
            images = category.images.all()
            categories_with_images.append({'category': category, 'images': images})

            rendered = {}
            rendered["service"] = ProjectGalleryPage.get_solo()
            rendered["services"] =  {index: service  for index, service in enumerate(core.models.Service.objects.all(), start=1)}
            rendered["categories_with_images"] = categories_with_images
            rendered["oldest_category"] = category.id
            rendered["gallery_categories"] = self.object.categories.all()
            ret.context_data.update(rendered)
            return render(self.request, 'core/pages/gallery_new.html', rendered)