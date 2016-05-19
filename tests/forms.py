from __future__ import absolute_import, unicode_literals

from django import VERSION, forms

from .models import (CustomPKFood, DirectCustomPKFood, DirectFood, Food,
                     OfficialFood)

fields = None
if VERSION >= (1, 6):
    fields = '__all__'


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = fields


class DirectFoodForm(forms.ModelForm):
    class Meta:
        model = DirectFood
        fields = fields


class DirectCustomPKFoodForm(forms.ModelForm):
    class Meta:
        model = DirectCustomPKFood
        fields = fields


class CustomPKFoodForm(forms.ModelForm):
    class Meta:
        model = CustomPKFood
        fields = fields


class OfficialFoodForm(forms.ModelForm):
    class Meta:
        model = OfficialFood
        fields = fields
