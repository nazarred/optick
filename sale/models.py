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
    comment = models.TextField(blank=True, null=True)

    def date_filter(first_date, last_date):
    	return SoldGlasses.objects.filter(sale_date__gte=first_date).exclude(sale_date__gte=last_date)

    def sale(glass):
        new_sale = SoldGlasses(
            kod=glass.kod,
            name=glass.name,
            price_opt=glass.price_opt,
            price_roz=glass.price_roz,
            dpt=glass.dpt,
            pcs=glass.pcs,
            comment=glass.comment
        )
        new_sale.save()

    def __str__(self):
        return '%s %s' % (self.name, self.kod)