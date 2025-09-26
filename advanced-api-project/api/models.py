from django.db import models

class Author(models.Model):
    """
    The Author model represents a writer.
    Each Author can write multiple Books (one-to-many relationship).
    """
    name = models.CharField(max_length=100)  # Author's name

    def __str__(self):
        return self.name  # Display author's name in admin and shell


class Book(models.Model):
    """
    The Book model represents a published book.
    Each Book is linked to a single Author through a ForeignKey.
    This creates a one-to-many relationship:
        - One Author can have many Books.
        - Each Book belongs to exactly one Author.
    """
    title = models.CharField(max_length=200)  # Title of the book
    publication_year = models.IntegerField()  # Year the book was published
    author = models.ForeignKey(
        Author,
        related_name="books",  # Allows reverse lookup: author.books.all()
        on_delete=models.CASCADE,  # If author is deleted, their books are deleted too
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
