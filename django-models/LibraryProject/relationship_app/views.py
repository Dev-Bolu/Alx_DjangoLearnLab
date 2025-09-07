from django.shortcuts import render
from .models import Author, Book, Library, Librarian
from django.views.generic import ListView, DetailView, CreateView, TemplateView
# Create your views here.
def book_list(request):
    # Query all books
    books = Book.objects.all()
    # Pass the books to the template
    return render(request, 'list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        