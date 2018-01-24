from django.db import models
from django.contrib import messages


class DptGlasses(models.Model):
    kod = models.CharField(max_length=15)
    name = models.CharField(max_length=20, blank=True, null=True)
    price_opt = models.FloatField()
    price_roz = models.IntegerField()
    dpt = models.FloatField()
    pcs = models.IntegerField()
    comment = models.TextField(blank=True, null=True)

    def inclement_and_save(self, kod, dpt):
        try:
            glass = DptGlasses.objects.get(kod=kod, dpt=dpt)
            glass.pcs += self.pcs
            glass.price_roz = self.price_roz
            glass.price_opt = self.price_opt
            glass.save()
        except Exception:
            return self.save()


    def messages_text(self, kod, dpt):
        try:
            glass = DptGlasses.objects.get(kod=kod, dpt=dpt)
            messages_dict = {'message': 'Окуляри %s змінені' % glass, 'second_message': 'ціни не змінилися'}
            if self.price_opt != glass.price_opt or self.price_roz != glass.price_roz:
                messages_dict['second_message'] = 'Роздрібна ціна: стара %d грн, нова %d грн;' \
                                                  ' оптова ціна стара %d грн, нова %d грн;' % (
                                                  glass.price_roz, self.price_roz,
                                                  glass.price_opt, self.price_opt)
        except Exception:
            messages_dict = {
                'message': 'Окуляри %s добавлені' % self,
                'second_message': 'Роздрібна ціна - %d грн,'
                ' оптова ціна - %d грн' % (
                self.price_roz, self.price_opt)
}
        return messages_dict

    def __str__(self):
        return '%s %s' % (self.name, self.kod)
