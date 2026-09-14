from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="home"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
]