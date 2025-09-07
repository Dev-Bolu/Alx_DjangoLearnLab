from django.shortcuts import render
from .models import Library, Book, Author, Librarian
from django.views.generic import DetailView
# Create your views here.
def book_list(request):
    # Query all books
    books = Book.objects.all()
    # Pass the books to the template
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        