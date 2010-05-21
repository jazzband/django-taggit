from django import forms

from taggit.tests.models import Food, DirectFood, CustomPKFood


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food

class DirectFoodForm(forms.ModelForm):
    class Meta:
        model = DirectFood

class CustomPKFoodForm(forms.ModelForm):
    class Meta:
        model = CustomPKFood
