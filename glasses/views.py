from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django import forms
from .models import DptGlasses
from django.views.generic.base import TemplateView
from sale.models import SoldGlasses
from django.contrib import messages
from .forms import GlassesModelForm, SearchModelForm, DateFilterModelForm

import datetime

date_today = datetime.date.today()

# datetime.date(1986, 7, 28)


class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        form = DateFilterModelForm()
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['glasses'] = SoldGlasses.objects.filter(sale_date__contains=date_today)
        context['date'] = date_today
        context['form'] = form
        for glass in context['glasses']:
            context['sum_price'] = context.get('sum_price', 0) + glass.price_roz*glass.pcs
            context['sum_pcs'] = context.get('sum_pcs', 0) + glass.pcs
        return context


def glasses_search(request):
    form = SearchModelForm()
    return render(request, 'glasses/search.html', {'form':form})


def glasses_list(request):
    try:
        form = SearchModelForm(request.GET)
        print(request.GET['kod'])
        glasses = DptGlasses.objects.all()
        if request.GET['kod']:
            glasses = glasses.filter(kod=request.GET['kod'])
        if request.GET['name']:
            glasses = glasses.filter(name__iexact=request.GET['name'])
        if request.GET['price_roz']:
            glasses = glasses.filter(price_roz=request.GET['price_roz'])
        if request.GET['dpt']:
            glasses = glasses.filter(dpt=request.GET['dpt'])
    except Exception:
        glass = DptGlasses.objects.get(id=request.GET['glass_id'])
        SoldGlasses.sale(glass)
        return redirect('index')
    return render(request, 'glasses/search.html', {'form':form, 'glasses': glasses})


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


