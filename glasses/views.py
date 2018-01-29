from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django import forms
from .models import DptGlasses
from django.views.generic.base import TemplateView
from sale.models import SoldGlasses
from django.contrib import messages
from .forms import GlassesModelForm, SearchModelForm, DateFilterModelForm
from .utils import date_from_post

import datetime

date_today = datetime.date.today()

# datetime.date(1986, 7, 28)

"""
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
"""


def home_page(request):
    form = DateFilterModelForm()
    glasses = SoldGlasses.objects.filter(sale_date__contains=date_today).order_by('-sale_date')
    context = {
        'form': form,
        'date': date_today,
    }
    if request.method == 'POST':
        first_date, last_date = date_from_post(request.POST)
        glasses = SoldGlasses.date_filter(first_date, last_date)
        context['first_date'], context['last_date'] = first_date, last_date
    context['glasses'] = glasses
    return render(request, 'index.html', context)


def glasses_search(request):
    form = SearchModelForm()
    return render(request, 'glasses/search.html', {'form': form})


def glasses_list(request):
    no_glass_message = None
    form = SearchModelForm(request.GET)
    glasses = DptGlasses.objects.all()
    if request.GET['kod']:
        glasses = glasses.filter(kod=request.GET['kod'])
    if request.GET['name']:
        glasses = glasses.filter(name__iexact=request.GET['name'])
    if request.GET['price_roz']:
        glasses = glasses.filter(price_roz=request.GET['price_roz'])
    if request.GET['dpt']:
        glasses = glasses.filter(dpt=request.GET['dpt'])
    if not glasses:
        no_glass_message = 'Окулярів з такими параметрими не знайдено'
    return render(request, 'glasses/search.html', {'form': form,
                                                   'glasses': glasses,
                                                   'no_glass_message': no_glass_message})


def glasses_add(request):
    if request.method == 'POST':
        kod, dpt = request.POST['kod'], request.POST['dpt']
        form = GlassesModelForm(request.POST)
        if form.is_valid():
            glass = form.save(commit=False)
            messages_dict = glass.messages_text(kod, dpt)
            glass.increment_and_save(kod, dpt)
            messages.success(request, messages_dict['message'])
            messages.success(request, messages_dict['second_message'])
            return redirect('index')
    else:
        form = GlassesModelForm()
    return render(request, 'glasses/add_form.html', {'form': form})
