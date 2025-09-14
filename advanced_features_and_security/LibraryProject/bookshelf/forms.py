# bookshelf/forms.py
from django import forms
from .models import Book
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        # Optionally restrict malicious characters or length:
        if len(title) > 200:
            raise forms.ValidationError("Title is too long.")
        return title

    def clean_publication_year(self):
        year = self.cleaned_data.get("publication_year")
        current_year = datetime.date.today().year
        if year is None:
            raise forms.ValidationError("Publication year is required.")
        if year < 0 or year > current_year + 1:
            raise forms.ValidationError("Enter a valid publication year.")
        return year
