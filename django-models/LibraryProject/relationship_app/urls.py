# relationship_app/urls.py
from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [          
    path("books/fbv/", list_books, name="list_books"),   # Function-based view
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),  # Library detail view
]
