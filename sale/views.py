from django.shortcuts import render, redirect
from glasses.models import DptGlasses
from .forms import SaleModelForm
from django.contrib import messages


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
            message = 'Окуляри %s продані, кількість %d ціна %d грн' % (glass, glass.pcs, glass.price_roz)
            messages.success(request, message)
            return redirect('index')

    return render(request, 'sale/sale.html', {'form': form})
