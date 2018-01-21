from django.db import models


class DptGlasses(models.Model):
    kod = models.CharField(max_length=15)
    name = models.CharField(max_length=20, blank=True, null=True)
    price_opt = models.FloatField()
    price_roz = models.IntegerField()
    dpt = models.FloatField()
    pcs = models.IntegerField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.name, self.kod)
