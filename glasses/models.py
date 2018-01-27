from django.core.exceptions import ValidationError
from django.db import models
from django.contrib import messages

from django import forms


class DptGlasses(models.Model):
    kod = models.CharField(max_length=15, verbose_name='Код')
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name="Ім'я")
    price_opt = models.FloatField(verbose_name='Оптова ціна', help_text='грн')
    price_roz = models.IntegerField(verbose_name='Роздрібна ціна', help_text='грн')
    dpt = models.FloatField(verbose_name='Діоптрії')
    pcs = models.PositiveIntegerField(verbose_name='Кількість', help_text='шт.')
    comment = models.TextField(blank=True, null=True, verbose_name='Примітка')

    def clean(self):
        data_list = [k/100 for k in range(-2000, 2000, 25)]
        if self.dpt not in data_list:
            raise ValidationError("Значення діоптрій не коректне (введіть значення від -20 до 20, наприклад '2,75', '-3.5')")

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
