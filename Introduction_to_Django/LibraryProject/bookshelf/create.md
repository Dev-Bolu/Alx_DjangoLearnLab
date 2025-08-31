'''python
from bookshelf.models import Book

book = Book.objects.create(title="1984", author='George Orwell',published_date=1847)
book
