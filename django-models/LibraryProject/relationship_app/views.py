'''
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
'''

from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

# ✅ Register View
class RegisterView(FormView):
    template_name = "relationship_app/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()  # save the user
        login(self.request, user)  # log them in
        return super().form_valid(form)


# ✅ Login View
class LoginView(FormView):
    template_name = "relationship_app/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)  # start session
        return super().form_valid(form)


# ✅ Logout View
class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = "relationship_app/logout.html"

    def get(self, request, *args, **kwargs):
        logout(request)  # clear session
        return super().get(request, *args, **kwargs)

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

# ✅ helper functions to check roles
def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and user.userprofile.role == 'Member'


# ✅ Admin View
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


# ✅ Librarian View
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


# ✅ Member View
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")
