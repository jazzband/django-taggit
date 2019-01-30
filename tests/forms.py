from __future__ import absolute_import, unicode_literals

from django import forms

from .models import CustomPKFood, DirectCustomPKFood, DirectFood, Food, OfficialFood


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = "__all__"


class DirectFoodForm(forms.ModelForm):
    class Meta:
        model = DirectFood
        fields = "__all__"


class DirectCustomPKFoodForm(forms.ModelForm):
    class Meta:
        model = DirectCustomPKFood
        fields = "__all__"


class CustomPKFoodForm(forms.ModelForm):
    class Meta:
        model = CustomPKFood
        fields = "__all__"


class OfficialFoodForm(forms.ModelForm):
    class Meta:
        model = OfficialFood
        fields = "__all__"
