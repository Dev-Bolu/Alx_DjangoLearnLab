from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from .models import Book, UserProfile
from .forms import ExampleForm



# --- BOOK VIEWS --- #

@login_required
@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    """List all books (requires 'can_view' permission)."""
    books = Book.objects.all()
    return render(request, "accounts/book_list.html", {"books": books})


@login_required
@permission_required("bookshelf.can_create", raise_exception=True)
def book_create(request):
    """Create a new book (requires 'can_create' permission)."""
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        publication_year = request.POST.get("publication_year")

        Book.objects.create(
            title=title,
            author=author,
            publication_year=publication_year,
        )
        return redirect("book_list")
    return render(request, "accounts/book_form.html")


@login_required
@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, pk):
    """Edit an existing book (requires 'can_edit' permission)."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.publication_year = request.POST.get("publication_year")
        book.save()
        return redirect("book_list")
    return render(request, "accounts/book_form.html", {"book": book})


@login_required
@permission_required("bookshelf.can_delete", raise_exception=True)
def book_delete(request, pk):
    """Delete a book (requires 'can_delete' permission)."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "accounts/book_confirm_delete.html", {"book": book})


# --- USER PROFILE VIEW --- #

@login_required
def user_profile(request):
    """View or update the logged-in user's profile."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.bio = request.POST.get("bio")
        profile.save()
        return redirect("user_profile")

    return render(request, "accounts/user_profile.html", {"profile": profile})

@login_required
def example_view(request):
    """Handle ExampleForm submission."""
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data["example_field"]
            return HttpResponse(f"You entered: {data}")
    else:
        form = ExampleForm()

    return render(request, "example_form.html", {"form": form})
