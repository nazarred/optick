from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse

from glasses.models import Glasses
from .forms import SaleModelForm
from django.contrib import messages

@login_required
def sale(request, pk):
    glass = Glasses.objects.get(id=pk)
    glass.pcs = 1
    form = SaleModelForm(instance=glass)
    if request.method == 'POST':
        form = SaleModelForm(request.POST)
        if form.is_valid():
            glass = form.save(commit=False)
            try:
                Glasses.objects.get(id=pk).decrement_or_delete(glass)
                glass.save()
                message = 'Окуляри %s продані, кількість %d ціна %d грн' % (glass, glass.pcs, glass.price_roz)
                messages.success(request, message)
                print(pk)
                return redirect('index')
            except ValidationError:
                message = 'Кількіть проданих окулярів не може перевищувати кількість окулярів в наявності'
                messages.success(request, message)
    return render(request, 'sale/sale.html', {'form': form})
