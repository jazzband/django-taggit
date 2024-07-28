from django.contrib import admin
from library_management.models import (
    Author,
    Book,
    BookType,
    ConditionTag,
    Magazine,
    PhysicalCopy,
)

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookType)
admin.site.register(Magazine)
admin.site.register(PhysicalCopy)
admin.site.register(ConditionTag)
