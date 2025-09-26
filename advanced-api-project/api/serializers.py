from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    - Converts Book objects into JSON format and vice versa.
    - Includes validation to prevent future publication years.
    """

    class Meta:
        model = Book
        fields = "__all__"  # Serialize all fields: title, publication_year, author

    def validate_publication_year(self, value):
        """
        Ensure publication year is not set in the future.
        Raises ValidationError if year > current year.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    - Serializes the Author's name.
    - Includes a nested list of the Author's related Books using BookSerializer.
    This demonstrates how relationships are represented in DRF.
    """
    books = BookSerializer(many=True, read_only=True)
    # 'books' comes from the related_name in the Book model (author.books.all())

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
