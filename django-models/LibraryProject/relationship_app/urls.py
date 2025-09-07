# relationship_app/urls.py
from django.urls import path
from .views import list_books, LibraryDetailView
from django.contrib.auth import views as auth_views
# from .views import register_view, login_view, logout_view
from django.views.generic import TemplateView
from .views import RegisterView, LoginView, LogoutView
urlpatterns = [
    # Function-based view: list all books
    path("books/", list_books, name="list_books"),
    
    # Class-based view: details of one library
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    
    
    #path("register/", register_view, name="register"),
    #path("login/", login_view, name="login"),
    #path("logout/", logout_view, name="logout"), 
    
    
    path("register/", RegisterView.as_view(), template_name="register"),
    path("login/", LoginView.as_view(), template_name="login"),
    path("logout/", LogoutView.as_view(), template_name="logout"),
    ]
    
