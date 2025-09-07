from django.shortcuts import render, redirect
from .models import Library, Book, Author, Librarian
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def list_books(request):
    # Query all books
    books = Book.objects.all()
    # Pass the books to the template
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        
# sign up

def register_view(request):
    if request.method == "POST":  # if the form is submitted
        form = UserCreationForm(request.POST)
        if form.is_valid():  # check if the data is valid
            user = form.save()  # save user to database
            login(request, user)  # log them in immediately
            return redirect("home")  # send to homepage
    else:
        form = UserCreationForm()  # empty form for GET request
    return render(request, "relationship_app/register.html", {"form": form})


# login

def login_view(request):
    if request.method == "POST":  # form submitted
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():  # check if username/password correct
            user = form.get_user()
            login(request, user)  # start session
            return redirect("home")
    else:
        form = AuthenticationForm()  # show empty form
    return render(request, "relationship_app/login.html", {"form": form})

# Logout
@login_required  # only logged-in users can log out
def logout_view(request):
    logout(request)  # remove session
    return render(request, "relationship_app/logout.html")
