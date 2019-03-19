from django import forms

from .models import (
    BlankTagModel,
    CustomPKFood,
    DirectCustomPKFood,
    DirectFood,
    Food,
    OfficialFood,
)


class BlankTagForm(forms.ModelForm):
    class Meta:
        model = BlankTagModel
        fields = "__all__"


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
