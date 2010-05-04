from django import forms

from taggit.tests.models import Food, DirectFood


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food

class DirectFoodForm(forms.ModelForm):
    class Meta:
        model = DirectFood
