from django.contrib import admin
from django.urls import re_path

from .views import FoodTagListView

urlpatterns = [
    re_path(
        r"^food/tags/(?P<slug>[a-z0-9_-]+)/$",
        FoodTagListView.as_view(),
        name="food-tag-list",
    ),
    re_path(r"^admin/", admin.site.urls),
]
