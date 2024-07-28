from django.db.models import Count
from django.db.models.functions import Lower
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AuthorForm, BookForm, PhysicalCopyForm
from .models import Author, Book, Magazine, PhysicalCopy


def home_page(request):
    # Number of books
    num_books = Book.objects.count()

    # Different genres represented
    genres = Book.tags.values("name").annotate(count=Count("name")).order_by("-count")

    # Condition of physical books
    condition_stats = (
        PhysicalCopy.objects.values("condition_tags__name")
        .annotate(count=Count("condition_tags"))
        .order_by("-count")
    )

    context = {
        "num_books": num_books,
        "genres": genres,
        "condition_stats": condition_stats,
    }

    return render(request, "library_management/home_page.html", context)


class BookListView(ListView):
    model = Book
    template_name = "library_management/book_list.html"
    context_object_name = "books"
    paginate_by = 20

    def get_ordering(self):
        ordering = self.request.GET.get("ordering", "name")
        if ordering == "name":
            return [Lower("name")]
        return [ordering]


class BookDetailView(DetailView):
    model = Book
    template_name = "library_management/book_detail.html"
    context_object_name = "book"


class BookCreateView(CreateView):
    model = Book
    template_name = "library_management/book_form.html"
    fields = ["name", "author", "published_date", "isbn", "summary", "tags"]
    success_url = reverse_lazy("book-list")


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "library_management/book_form.html"

    def get_success_url(self):
        return reverse("book-detail", kwargs={"pk": self.object.pk})


class AuthorListView(ListView):
    model = Author
    template_name = "library_management/author_list.html"
    context_object_name = "authors"
    ordering = ["last_name", "first_name"]


class AuthorDetailView(DetailView):
    model = Author
    template_name = "library_management/author_detail.html"
    context_object_name = "author"


class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = "library_management/author_form.html"
    context_object_name = "author"


class MagazineListView(BookListView):
    model = Magazine
    template_name = "library_management/magazine_list.html"
    context_object_name = "magazines"


class MagazineDetailView(BookDetailView):
    model = Magazine
    template_name = "library_management/book_detail.html"
    context_object_name = "book"


class MagazineCreateView(BookCreateView):
    model = Magazine
    template_name = "library_management/book_form.html"
    success_url = reverse_lazy("magazine-list")


class MagazineUpdateView(BookUpdateView):
    model = Magazine
    form_class = BookForm
    template_name = "library_management/book_form.html"
    context_object_name = "book"

    def get_success_url(self):
        return reverse("magazine-detail", kwargs={"pk": self.object.pk})


class PhysicalCopyUpdateView(UpdateView):
    model = PhysicalCopy
    form_class = PhysicalCopyForm
    template_name = "library_management/physical_copy_form.html"

    def get_success_url(self):
        return reverse("book-detail", kwargs={"pk": self.object.book.pk})
