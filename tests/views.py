from django.views.generic.list import ListView

from .models import Food

from taggit.views import TagListMixin


class FoodTagListView(TagListMixin, ListView):
    model = Food
