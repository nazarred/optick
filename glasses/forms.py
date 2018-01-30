from django import forms
from django.forms import SplitDateTimeWidget, SelectDateWidget
import datetime

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
    kod = forms.CharField(max_length=15, required=False, label='Код')
    name = forms.CharField(max_length=20, required=False, label="Ім'я")
    price_roz = forms.IntegerField(required=False, label='Роздрібна ціна')
    dpt = forms.FloatField(required=False, label='Діоптрії')


    def clean(self):
        data_list = [k/100 for k in range(-2000, 2000, 25)]
        data_list.append(None)
        if self.cleaned_data.get('dpt') not in data_list:
            raise forms.ValidationError('Значення діоптрій не коректне (наприклад 1,75)')
        return self.cleaned_data


class DateFilterModelForm(forms.Form):
    years = range(2017, 2025)
    months = {
        1: 'Січень', 2: 'Лютий', 3: 'Березень', 4: 'Квітень',
        5: 'Травень', 6: 'Червень', 7: 'Липень', 8: 'Серпень',
        9: 'Вересень', 10: 'Жовтень', 11: 'Листопад', 12: 'Грудень'
    }
    first_date = forms.DateField(
        label='Початкова дата',
        widget=SelectDateWidget(months=months, years=years),
        initial=datetime.date.today()
    )
    last_date = forms.DateField(
        label='Кінцева дата',
        widget=SelectDateWidget(months=months, years=years),
        initial=datetime.date.today()
    )
