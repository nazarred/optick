from django import forms
from .models import DptGlasses


class GlassesModelForm(forms.ModelForm):
    class Meta:
        model = DptGlasses
        exclude = []


class SearchModelForm(forms.Form):
    kod = forms.CharField(max_length=15, required=False)
    name = forms.CharField(max_length=20, required=False)
    price_roz = forms.IntegerField(required=False)
    dpt = forms.FloatField(required=False)
