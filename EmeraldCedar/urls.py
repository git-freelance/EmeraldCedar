"""EmeraldCedar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.defaults import page_not_found

from jet.dashboard.dashboard_modules import google_analytics_views
from core.views import redirect_login
from pages.views import IndexView, MapDetailView, ServiceDetailView, FeaturedProjectsView, ProjectDetailView, \
    CustomPageDetailView, ContactView, ThankYouView, TestimonialsListView, GalleryView
from blog.views import BlogMainPageView, PostsByMonthView, PostDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('redactor/', include('redactor.urls')),
    path('chaining/', include('smart_selects.urls')),

    path('accounts/email/', page_not_found, {'exception': Exception('Not Found')}),
    path('accounts/signup/', page_not_found, {'exception': Exception('Not Found')}),
    path('accounts/', include('allauth.urls')),

    path('dash/', include('authorization.urls')),

    path('', IndexView.as_view(), name='index'),
    path('redirect/', redirect_login, name='redirect_login'),
    path('testimonials/', TestimonialsListView.as_view(), name='testimonials'),
    path('map/', MapDetailView.as_view(), name='map'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('thank-you/', ThankYouView.as_view(), name='thankyou'),
    # path('featured-projects/', FeaturedProjectsView.as_view(), name='featured_projects'),
    path('projects/', FeaturedProjectsView.as_view(), name='featured_projects'),
    path('service/<slug:slug>/', ServiceDetailView.as_view(), name='service'),
    path('project/<slug:slug>/', ProjectDetailView.as_view(), name='project'),
    path('page/<slug:slug>/', CustomPageDetailView.as_view(), name='custom_page'),

    path('blog/', BlogMainPageView.as_view(), name='blog'),
    path('blog/<int:year>/<int:month>/', PostsByMonthView.as_view(), name='posts_by_month'),
    path('blog/<slug:slug>/', PostDetailView.as_view(), name='blog_post'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
