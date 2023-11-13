from django.views.generic import FormView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.dates import MonthArchiveView
from django.urls import reverse_lazy

from core.forms import ContactForm

from .models import BlogPage, Post


class BlogMainPageView(ListView):
    template_name = 'blog/pages/blog.html'
    model = Post
    paginate_by = 12

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page'] = BlogPage.get_solo()
        return ctx


class PostsByMonthView(MonthArchiveView):
    template_name = 'blog/pages/blog.html'
    queryset = Post.objects.all()
    date_field = 'created_at'
    allow_future = True
    month_format = '%m'
    context_object_name = 'posts'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page'] = BlogPage.get_solo()
        return ctx


class PostDetailView(SingleObjectMixin, FormView):
    template_name = 'blog/pages/post_detail.html'
    model = Post
    form_class = ContactForm
    success_url = reverse_lazy('thankyou')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        solo = BlogPage.get_solo()
        ctx['solo'] = solo
        ctx['banner'] = self.object.banner or solo.banner or None
        ctx['archives'] = Post.objects.dates('created_at', 'month', order='DESC')
        ctx['latest_news'] = Post.objects.exclude(pk=self.object.pk)[:5]
        return ctx
