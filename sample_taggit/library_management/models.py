import uuid

from django.db import models
from django.urls import reverse

from taggit.managers import TaggableManager
from taggit.models import TagBase, TaggedItemBase


class BookTypeChoices(models.TextChoices):
    HARDCOVER = "HC", "Hardcover"
    PAPERBACK = "PB", "Paperback"
    EBOOK = "EB", "E-book"
    AUDIOBOOK = "AB", "Audiobook"
    MAGAZINE = "MG", "Magazine"


class BookType(TagBase):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Book Type"
        verbose_name_plural = "Book Types"


class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    published_date = models.DateField(null=True)
    isbn = models.CharField(max_length=17, unique=True)
    summary = models.TextField()
    tags = TaggableManager()

    @property
    def title(self):
        return self.name

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


class MagazineManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                physical_copies__book_type__name="Magazine",
                physical_copies__isnull=False,
            )
            .distinct()
        )


class Magazine(Book):
    objects = MagazineManager()

    class Meta:
        proxy = True

    @property
    def title(self):
        return f"{self.name} Edition: {self.published_date.strftime('%B %Y')}"


class Author(models.Model):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField()
    biography = models.TextField()
    tags = TaggableManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("author-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.full_name


class ConditionTag(TagBase):
    class Meta:
        verbose_name = "Condition Tag"
        verbose_name_plural = "Condition Tags"
        ordering = ["name"]


class ConditionTaggedItem(TaggedItemBase):
    tag = models.ForeignKey(
        ConditionTag, related_name="tagged_items", on_delete=models.CASCADE
    )
    content_object = models.ForeignKey("PhysicalCopy", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Condition Tagged Item"
        verbose_name_plural = "Condition Tagged Items"


class PhysicalCopy(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="physical_copies"
    )
    barcode = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    book_type = models.ForeignKey(BookType, on_delete=models.CASCADE)
    condition_tags = TaggableManager(through=ConditionTaggedItem, blank=True)

    def __str__(self):
        return f"{self.book.name} - {self.barcode}"

    class Meta:
        verbose_name = "Physical Copy"
        verbose_name_plural = "Physical Copies"
