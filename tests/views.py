from django.views.generic.list import ListView

from taggit.views import TagListMixin

from .models import Food


class FoodTagListView(TagListMixin, ListView):
    model = Food
