from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from datetime import datetime

# ✅ ListView → Get all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# ✅ DetailView → Get a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# ✅ CreateView → Add a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # only logged-in users can create

    def perform_create(self, serializer):
        # Example: add extra validation or auto-assign fields
        if serializer.validated_data["publication_year"] > datetime.now().year:
            raise ValueError("Publication year cannot be in the future.")
        serializer.save()



# ✅ UpdateView → Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # only logged-in users can update

    def perform_update(self, serializer):
        if serializer.validated_data.get("publication_year") and serializer.validated_data["publication_year"] > datetime.now().year:
            raise ValueError("Publication year cannot be in the future.")
        serializer.save()


# ✅ DeleteView → Remove a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # only logged-in users can delete

# Book CRUD Views:
# - BookListView → GET all books
# - BookDetailView → GET single book by ID
# - BookCreateView → POST new book (auth required)
# - BookUpdateView → PUT/PATCH existing book (auth required)
# - BookDeleteView → DELETE a book (auth required)
#
# Permissions:
# - Read (list/retrieve) is open
# - Write (create/update/delete) requires authentication
#
# Validation:
# - publication_year cannot be in the future
