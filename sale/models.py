from django.db import models
import datetime


class SoldGlasses(models.Model):
    kod = models.CharField(max_length=15)
    name = models.CharField(max_length=20, blank=True, null=True)
    dpt = models.FloatField(blank=True, null=True)
    pcs = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)
    price_opt = models.FloatField()
    price_roz = models.IntegerField()
    glass_type = models.CharField(max_length=20, verbose_name='Тип')
    comment = models.TextField(blank=True, null=True)

    def date_filter(first_date, last_date):
        last_date = datetime.date(last_date.year, last_date.month, last_date.day+1)
        return SoldGlasses.objects.filter(sale_date__gte=first_date).exclude(sale_date__gte=last_date).order_by('-sale_date')

    def __str__(self):
        return '%s %s' % (self.name, self.kod)