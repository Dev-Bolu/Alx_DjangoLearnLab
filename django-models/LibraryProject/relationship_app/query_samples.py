import os
import django

# Setup Django environment (only needed if running as standalone script)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian



def run_queries():
    author_name = "J.K. Rowling"
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)  # filter all books with this author
    print(f"Books by {author_name}: {[book.title for book in books_by_author]}")

    # 2. List all books in a library
    library_name = "Central Library"
    library = Library.objects.get(name=library_name)
    books_in_library = library.books.all()
    print(f"Books in {library_name}: {[book.title for book in books_in_library]}")

    # 3. Retrieve the librarian for a library
    librarian = library.librarian
    print(f"Librarian of {library_name}: {librarian.name}")


if __name__ == "__main__":
    run_queries()