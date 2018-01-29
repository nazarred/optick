from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse

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
            try:
                DptGlasses.objects.get(id=pk).decrement_or_delete(glass)
                glass.save()
                message = 'Окуляри %s продані, кількість %d ціна %d грн' % (glass, glass.pcs, glass.price_roz)
                messages.success(request, message)
                return reverse('sale:glass_sale', kwargs={'pk': pk})
            except ValidationError:
                message = 'Кількіть проданих окулярів не може перевищувати кількість окулярів в наявності'
                messages.success(request, message)
                return render(request, 'sale/sale.html', {'form': form})
    return render(request, 'sale/sale.html', {'form': form})
