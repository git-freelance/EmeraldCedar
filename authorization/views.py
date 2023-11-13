import calendar

from django.utils import timezone
from django.views.generic import RedirectView, DetailView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden

from allauth.account.views import PasswordChangeView
from dateutil.relativedelta import relativedelta

from .models import Project


@method_decorator(login_required, name='dispatch')
class DashIndexView(RedirectView):
    pattern_name = 'dash_projects'


@method_decorator(login_required, name='dispatch')
class DashProjectListView(ListView):
    template_name = 'authorization/pages/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        if self.request.user.is_admin():
            return Project.objects.all()
        return self.request.user.projects.all()


@method_decorator(login_required, name='dispatch')
class DashProjectDetailView(DetailView):
    template_name = 'authorization/pages/project_detail.html'
    model = Project

    def dispatch(self, request, *args, **kwargs):
        ret = super().dispatch(request, *args, **kwargs)
        if self.request.user.is_admin() or self.object.user == request.user:
            return ret
        return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        start_date = self.object.warranty_start_date
        end_date = self.object.warranty_end_date
        today = timezone.now().date()
        allow_chart = False
        if start_date and end_date and end_date > today:
            left = relativedelta(end_date, today)
            allow_chart = True

            ctx['years_left'] = left.years
            ctx['months_left'] = left.months
            ctx['days_left'] = left.days

            ctx['years_in_percent'] = 100 / (end_date.year - start_date.year) * left.years if left.years else 0
            ctx['months_in_percent'] = 100 / 12 * left.months if left.months else 0
            ctx['days_in_percent'] = 100 / calendar.monthrange(today.year, today.month)[1] * left.days if left.days else 0

        ctx['allow_chart'] = allow_chart
        return ctx


@method_decorator(login_required, name='dispatch')
class DashPasswordView(PasswordChangeView):
    template_name = 'authorization/pages/dash_password.html'
    success_url = reverse_lazy('dash_password')

    def form_valid(self, *args):
        messages.info(self.request, 'Your password is now changed.', extra_tags='password_changed')
        return super().form_valid(*args)
