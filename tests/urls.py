from django.conf.urls import url
from django.contrib import admin

from .views import FoodTagListView

urlpatterns = [
    url(
        r"^food/tags/(?P<slug>[a-z0-9_-]+)/$",
        FoodTagListView.as_view(),
        name="food-tag-list",
    ),
    url(r"^admin/", admin.site.urls),
]
