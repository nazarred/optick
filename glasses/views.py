from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django import forms
from .models import DptGlasses
from django.views.generic.base import TemplateView
from sale.models import SoldGlasses
from django.contrib import messages

import datetime

date_today = datetime.date(2018, 1, 22)


class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['sold_glasses'] = SoldGlasses.objects.filter(sale_date__contains=date_today)
        context['date_today'] = date_today

        #datetime.date(1986, 7, 28)

        for glass in context['sold_glasses']:
            context['sum_price'] = context.get('sum_price', 0) + glass.price_roz*glass.pcs
            context['sum_pcs'] = context.get('sum_pcs', 0) + glass.pcs
        return context


def glasses_search(request):
    return render(request, 'glasses/glass.html')


class GlassesModelForm(forms.ModelForm):
    class Meta:
        model = DptGlasses
        exclude = []


class GlassesCreateView(CreateView):
    form_class = GlassesModelForm
    template_name = 'glasses/add_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        message = 'Окуляри %s %s добавлені' % (self.request.POST['name'], self.request.POST['kod'])
        messages.success(self.request, message)
        return response


def glasses_add(request):
    if request.method == 'POST':
        kod, dpt = request.POST['kod'], request.POST['dpt']
        # якщо окуляри з таким кодом і діоптріями вже є збільшуємо кількісь в існуючумо екземплярі
        if DptGlasses.objects.filter(kod=kod, dpt=dpt):
            inst = DptGlasses.objects.filter(kod=kod, dpt=dpt).get()
            default_pcs = inst.pcs
            old_price_roz = inst.price_roz
            old_price_opt = inst.price_opt
            form = GlassesModelForm(request.POST, instance=inst)
            if form.is_valid():
                glass = form.save(commit=False)
                glass.pcs = default_pcs + int(request.POST['pcs'])
                glass.save()
                message = 'Окуляри %s %s змінені' % (request.POST['name'], request.POST['kod'])
                messages.success(request, message)
                second_message = 'ціни не змінилися'
                if old_price_opt != glass.price_opt or old_price_roz != glass.price_roz:
                    second_message = 'Роздрібна ціна: нова %d грн, стара %d грн;' \
                                     ' оптова ціна нова %d грн, стара %d грн;' % (glass.price_roz, old_price_roz,
                                                                                  glass.price_opt, old_price_opt
                                                                                  )
                messages.success(request, second_message)
                return redirect('index')
        form = GlassesModelForm(request.POST)
        # якщо окулярів немає - створюємо новий інстанс
        if form.is_valid():
            instance = form.save()
            message = 'Окуляри %s %s добавлені' % (request.POST['name'], request.POST['kod'])
            messages.success(request, message)
            return redirect('index')
    else:
        form = GlassesModelForm()
    return render(request, 'glasses/add_form.html', {'form': form})
