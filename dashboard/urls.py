from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="home"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/users/add/", views.admin_user_add, name="admin_user_add"),
    path("admin/users/<int:pk>/edit/", views.admin_user_edit, name="admin_user_edit"),
    path("admin/users/<int:pk>/delete/", views.admin_user_delete, name="admin_user_delete"),
]
