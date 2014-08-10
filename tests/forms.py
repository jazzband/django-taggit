from __future__ import absolute_import, unicode_literals

from django import forms, VERSION

from .models import CustomPKFood, DirectFood, Food, OfficialFood

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

class CustomPKFoodForm(forms.ModelForm):
    class Meta:
        model = CustomPKFood
        fields = fields

class OfficialFoodForm(forms.ModelForm):
    class Meta:
        model = OfficialFood
        fields = fields
