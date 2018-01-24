from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django import forms
from .models import DptGlasses
from django.views.generic.base import TemplateView
from sale.models import SoldGlasses
from django.contrib import messages
from .forms import GlassesModelForm

import datetime

date_today = datetime.date(2018, 1, 22)

# datetime.date(1986, 7, 28)


class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['sold_glasses'] = SoldGlasses.objects.filter(sale_date__contains=date_today)
        context['date_today'] = date_today
        for glass in context['sold_glasses']:
            context['sum_price'] = context.get('sum_price', 0) + glass.price_roz*glass.pcs
            context['sum_pcs'] = context.get('sum_pcs', 0) + glass.pcs
        return context


def glasses_search(request):
    return render(request, 'glasses/glass.html')




"""
створює об'єкт, але не змінює

class GlassesCreateView(CreateView):
    form_class = GlassesModelForm
    template_name = 'glasses/add_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        message = 'Окуляри %s %s добавлені' % (self.request.POST['name'], self.request.POST['kod'])
        messages.success(self.request, message)
        return response
"""

def glasses_add(request):
    if request.method == 'POST':
        kod, dpt = request.POST['kod'], request.POST['dpt']
        form = GlassesModelForm(request.POST)
        if form.is_valid():
            glass = form.save(commit=False)
            messages_dict = glass.messages_text(kod, dpt)
            glass.inclement_and_save(kod, dpt)
            messages.success(request, messages_dict['message'])
            messages.success(request, messages_dict['second_message'])
            return redirect('index')
    else:
        form = GlassesModelForm()
    return render(request, 'glasses/add_form.html', {'form': form})


