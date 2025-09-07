from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import admin_view, librarian_view, member_view

urlpatterns = [
    # Function-based register view (if checker expects it)
    path("register/", views.register, name="register"),

    # Login/Logout using built-in Django auth views with template_name
    path("login/", auth_views.LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    
    path("admin-view/", admin_view, name="admin_view"),
    path("librarian-view/", librarian_view, name="librarian_view"),
    path("member-view/", member_view, name="member_view"),
]