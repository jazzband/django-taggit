from django import forms

from taggit.tests.models import Food


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
