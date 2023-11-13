from django.urls import path

from .views import DashIndexView, DashProjectListView, DashProjectDetailView, DashPasswordView

urlpatterns = [
    path('', DashIndexView.as_view(), name='dash_index'),
    path('projects/', DashProjectListView.as_view(), name='dash_projects'),
    path('project/<int:pk>/', DashProjectDetailView.as_view(), name='dash_project'),
    path('password/', DashPasswordView.as_view(), name='dash_password'),
]
