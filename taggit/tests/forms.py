from taggit.forms import TaggableForm

from taggit.tests.models import Food


class FoodForm(TaggableForm):
    class Meta:
        model = Food
