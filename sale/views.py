from django.shortcuts import render
from glasses.models import DptGlasses
from .forms import SaleModelForm


def sale(request, pk):
    glass = DptGlasses.objects.get(id=pk)
    glass.pcs = 1
    form = SaleModelForm(instance=glass)
    if request.method == 'POST':
        form = SaleModelForm(request.POST)
        if form.is_valid():
            glass = form.save(commit=False)
            #треба ще добавити функції видалення або зменшення кількості в моделі DptGlasses
            glass.save()
    return render(request, 'sale/sale.html', {'form': form})
