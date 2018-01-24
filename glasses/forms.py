from django import forms
from .models import DptGlasses


class GlassesModelForm(forms.ModelForm):
    class Meta:
        model = DptGlasses
        exclude = []