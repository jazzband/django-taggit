from django.conf.urls import url

from .tests import FoodTagListView

urlpatterns = [
    url(r'^food/tags/(?P<slug>[a-z0-9_-]+)/$', FoodTagListView.as_view(),
        name='food-tag-list'),
]
