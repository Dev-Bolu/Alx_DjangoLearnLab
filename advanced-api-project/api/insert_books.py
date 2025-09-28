from django.core.management.base import BaseCommand
from .models import Author, Book


class Command(BaseCommand):
    help = "Insert sample authors and their books into the database"

    def handle(self, *args, **kwargs):
        # Dictionary: Author -> list of books
        sample_data = {
            "Andrew Hunt": [
                {"title": "The Pragmatic Programmer", "publication_year": 1999},
            ],
            "Robert C. Martin": [
                {"title": "Clean Code", "publication_year": 2008},
                {"title": "Clean Architecture", "publication_year": 2017},
            ],
            "Thomas H. Cormen": [
                {"title": "Introduction to Algorithms", "publication_year": 2009},
            ],
            "Eric Matthes": [
                {"title": "Python Crash Course", "publication_year": 2015},
            ],
            "William S. Vincent": [
                {"title": "Django for Beginners", "publication_year": 2018},
                {"title": "Django for Professionals", "publication_year": 2020},
            ],
        }

        for author_name, books in sample_data.items():
            author, _ = Author.objects.get_or_create(name=author_name)
            for book in books:
                book_obj, created = Book.objects.get_or_create(
                    title=book["title"],
                    publication_year=book["publication_year"],
                    author=author,
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Inserted: {book_obj.title} by {author.name}"
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Already exists: {book_obj.title} by {author.name}"
                    ))
