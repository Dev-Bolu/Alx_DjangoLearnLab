from django.shortcuts import render
from .models import Book
from .models import Library

# Create your views 

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

