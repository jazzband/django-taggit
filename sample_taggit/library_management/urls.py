from django.urls import path

from .views import (
    AuthorDetailView,
    AuthorListView,
    AuthorUpdateView,
    BookCreateView,
    BookDetailView,
    BookListView,
    BookUpdateView,
    MagazineCreateView,
    MagazineDetailView,
    MagazineListView,
    MagazineUpdateView,
    PhysicalCopyUpdateView,
    home_page,
)

urlpatterns = [
    path("", home_page, name="home_page"),
    path("book_list", BookListView.as_view(), name="book-list"),
    path("book/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("book/new/", BookCreateView.as_view(), name="book-create"),
    path("book/<int:pk>/edit/", BookUpdateView.as_view(), name="book-update"),
    path("authors/", AuthorListView.as_view(), name="author-list"),
    path("authors/<int:pk>/", AuthorDetailView.as_view(), name="author-detail"),
    path("authors/<int:pk>/edit/", AuthorUpdateView.as_view(), name="author-update"),
    path("magazines/", MagazineListView.as_view(), name="magazine-list"),
    path("magazine/<int:pk>/", MagazineDetailView.as_view(), name="magazine-detail"),
    path("magazine/new/", MagazineCreateView.as_view(), name="magazine-create"),
    path(
        "magazine/<int:pk>/edit/", MagazineUpdateView.as_view(), name="magazine-update"
    ),
    path(
        "physical_copy/<int:pk>/edit/",
        PhysicalCopyUpdateView.as_view(),
        name="physical-copy-update",
    ),
]
