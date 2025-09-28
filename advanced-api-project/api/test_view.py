from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Test suite for the Book API endpoints.
    Covers CRUD, filtering, searching, ordering, and permissions.
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        # Create an author
        self.author = Author.objects.create(name="John Doe")

        # Create a book
        self.book = Book.objects.create(
            title="Django Basics",
            publication_year=2023,
            author=self.author
        )

        # Endpoints
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", args=[self.book.id])
        self.create_url = reverse("book-create")
        self.update_url = reverse("book-update")
        self.delete_url = reverse("book-delete")

    # -----------------------
    # CRUD TESTS
    # -----------------------

    def test_list_books(self):
        """Anyone should be able to list books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Django Basics", str(response.data))

    def test_retrieve_single_book(self):
        """Retrieve a single book by ID"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Django Basics")

    def test_create_book_authenticated(self):
        """Only authenticated users can create"""
        self.client.login(username="testuser", password="testpass123")
        data = {
            "title": "New Book",
            "publication_year": 2022,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        """Unauthenticated users cannot create"""
        data = {
            "title": "Unauthorized Book",
            "publication_year": 2021,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        """Authenticated users can update a book"""
        self.client.login(username="testuser", password="testpass123")
        data = {
            "id": self.book.id,
            "title": "Updated Django",
            "publication_year": 2024,
            "author": self.author.id
        }
        response = self.client.put(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Django")

    def test_delete_book_authenticated(self):
        """Authenticated users can delete a book"""
        self.client.login(username="testuser", password="testpass123")
        data = {"id": self.book.id}
        response = self.client.delete(self.delete_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_unauthenticated(self):
        """Unauthenticated users cannot delete a book"""
        data = {"id": self.book.id}
        response = self.client.delete(self.delete_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -----------------------
    # FILTER / SEARCH / ORDER TESTS
    # -----------------------

    def test_filter_books_by_year(self):
        """Filter books by publication year"""
        response = self.client.get(f"{self.list_url}?publication_year=2023")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_title(self):
        """Search books by title"""
        response = self.client.get(f"{self.list_url}?search=Django")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Django Basics", str(response.data))

    def test_order_books_by_year(self):
        """Order books by publication year"""
        # Add another book with different year
        Book.objects.create(title="Another Book", publication_year=2020, author=self.author)
        response = self.client.get(f"{self.list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # First book in response should be the older one (2020)
        self.assertEqual(response.data[0]["publication_year"], 2020)
