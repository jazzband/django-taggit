from __future__ import unicode_literals, absolute_import

from django import forms

from .models import Food, DirectFood, CustomPKFood, OfficialFood


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'

class DirectFoodForm(forms.ModelForm):
    class Meta:
        model = DirectFood
        fields = '__all__'

class CustomPKFoodForm(forms.ModelForm):
    class Meta:
        model = CustomPKFood
        fields = '__all__'

class OfficialFoodForm(forms.ModelForm):
    class Meta:
        model = OfficialFood
        fields = '__all__'
