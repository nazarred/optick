from django.shortcuts import render
from .models import DptGlasses
from django.views.generic.base import TemplateView
from sale.models import SoldGlasses
import datetime




class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['sold_glasses'] = SoldGlasses.objects.filter(sale_date__contains=datetime.date.today())
        #datetime.date(1986, 7, 28)
        for glass in context['sold_glasses']:
        	context['sum_price'] = context.get('sum_price', 0) + glass.price_roz*glass.pcs
        	context['sum_pcs'] = context.get('sum_pcs', 0) + glass.pcs
        return context


def glasses_search(request):
    return render(request, 'glasses/glass.html')

