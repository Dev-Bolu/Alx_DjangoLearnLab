# relationship_app/urls.py
from django.urls import path
from .views import book_list, BookListView,LibraryDetailView

urlpatterns = [
    path("books/fbv/", book_list, name="book_list_fbv"),   # Function-based view
    path("books/cbv/", BookListView.as_view(), name="book_list_cbv"),  # Class-based view
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),  # Library detail view
]
