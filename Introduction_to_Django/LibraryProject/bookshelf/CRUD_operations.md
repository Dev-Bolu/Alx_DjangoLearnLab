# CRUD Operation in Django shell

## 1. Create
### Command:
'''python
from bookshelf.models import Book
book = Book.objects.create(title='1984', author="George Orwell", publication_year=1949)
book

# Output
<Book: 1984 by George Orwell>


## 2. Retrieve
### Command:
Book.objects.all()

retrieve_book = Book.objects.get(id=book.id)
retrieve_book.title, retrieved_book.author,
retrieved_book.publication_year
# Output
<QuerysET [<Book: 1984 by George Orwell>]>
('1984', 'George Orwell', 1949)


## 3. Update
### Command:
book.title = "Nineteen Eight-Four"
book.save()

book

# Output

<Book: Nineteen Eight-Four by George Orwell>

## 4. Delete
### Command:
book.delete()
Book.objects.all()

# Output
(1, {'bookshelf.Book': 1})
<QuerySet []>