from django import forms
from .models import DptGlasses


class GlassesModelForm(forms.ModelForm):
    class Meta:
        model = DptGlasses
        exclude = []



"""
class SearchModelForm(forms.ModelForm):
    class Meta:
        model = DptGlasses
        exclude = ['price_opt', 'pcs', 'comment']
"""


class SearchModelForm(forms.Form):
    kod = forms.CharField(max_length=15, required=False, )
    name = forms.CharField(max_length=20, required=False)
    price_roz = forms.IntegerField(required=False)
    dpt = forms.FloatField(required=False)


    def clean(self):
        data_list = [k/100 for k in range(-2000, 2000, 25)]
        data_list.append(None)
        if self.cleaned_data.get('dpt') not in data_list:
            raise forms.ValidationError('Значення діоптрій не коректне (наприклад 1,75)')
        return self.cleaned_data
