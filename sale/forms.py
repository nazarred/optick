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
            'dpt': TextInput(attrs={'readonly': 'readonly'}),
            'price_opt': HiddenInput,
        }

    def clean(self):
        if self.cleaned_data.get('pcs') <= 0:
            raise forms.ValidationError('Кількість проданих окулярів не може бути меншою 0 або дорівнювати 0')
        return self.cleaned_data