from __future__ import unicode_literals, absolute_import

from django import forms, VERSION

from .models import Food, DirectFood, CustomPKFood, OfficialFood


fields = None
if VERSION >= (1,6):
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
