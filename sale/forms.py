from django import forms
from django.forms import TextInput, NumberInput, HiddenInput
from .models import SoldGlasses


class SaleModelForm(forms.ModelForm):
    class Meta:
        model = SoldGlasses
        exclude = []
        widgets = {
            'kod': TextInput(attrs={'readonly': 'readonly'}),
            'name': TextInput(attrs={'readonly': 'readonly'}),
            'dpt': NumberInput(attrs={'readonly': 'readonly'}),
            'price_opt': HiddenInput,
        }
