# relationship_app/urls.py
from django.urls import path
from .views import list_books, LibraryDetailView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Function-based view: list all books
    path("books/", list_books, name="list_books"),

    # Class-based view: details of one library
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    
    # If you want to customize login/logout views, you can do so here
    path('account/login/', auth_views.LoginView.as_view(), name='login'),
    path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]