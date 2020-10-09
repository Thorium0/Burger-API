from django import forms
from .models import CustomBurger

class CustomBurgerCreationForm(forms.ModelForm):
    class Meta:
        model = CustomBurger
        fields = ['title', 'image', 'price', 'meats', 'buns', 'condiments', 'salads']
